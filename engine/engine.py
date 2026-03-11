"""Core Engine — game loop, state management, rendering coordination."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

import tcod.console

from ui.message_log import MessageLog
from ui import color as Color

if TYPE_CHECKING:
    from entities.actor import Actor
    from world.game_map import GameMap


class Engine:
    def __init__(
        self,
        player: Actor,
        game_map: GameMap,
        seed: Optional[int] = None,
        char_class: Optional[object] = None,
    ) -> None:
        self.player = player
        self.game_map = game_map
        self.char_class = char_class

        self.rng = random.Random(seed)
        self.seed = seed if seed is not None else 0

        self.message_log = MessageLog()
        self.turn_count = 0

        # Economy / meta state (populated by subsystems)
        self.heat: int = 0          # 0-100
        self.cash: int = 100
        self.district: str = "West Bottoms"

        # Crew
        from components.crew_member import CrewRoster
        self.crew: CrewRoster = CrewRoster()

        # Phase 15: Level tracking
        self._last_level: int = 1

    def handle_enemy_turns(self) -> None:
        for actor in list(self.game_map.actors):
            if actor is self.player:
                continue
            if actor.ai:
                actor.ai.perform(self)
        # Phase 15: check for level-up after enemy turns
        self._check_level_up()

    def _check_level_up(self) -> None:
        """Check if the player has levelled up and fire the perk screen if so."""
        level = self._get_player_level()
        if level > self._last_level:
            self._last_level = level
            self.message_log.add_message(
                f"You've grown as an operator. Level {level}! Pick a perk.",
                fg=Color.GOLD,
            )
            # Perk screen fired from event_handler after turn to avoid circular import

    def _get_player_level(self) -> int:
        """Compute current level from jobs_completed and total rep."""
        jobs = getattr(self, "jobs_completed", 0)
        standing = getattr(self.player, "faction_standing", None)
        total_rep = sum(standing.rep.values()) if standing else 0
        return 1 + (jobs // 5) + (total_rep // 50)

    @property
    def pending_level_up(self) -> bool:
        """True when a level-up is waiting for perk selection."""
        return self._get_player_level() > self._last_level

    def consume_level_up(self) -> None:
        """Acknowledge a level-up (call after perk screen)."""
        self._last_level = self._get_player_level()

    def update_fov(self) -> None:
        self.game_map.compute_fov(self.player.x, self.player.y)

    def render(self, console: tcod.console.Console) -> None:
        from ui.panels import render_all
        self.game_map.render(console)
        render_all(console, self)

    # -----------------------------------------------------------------------
    # Serialization (Phase 14)
    # -----------------------------------------------------------------------

    def to_dict(self) -> dict:
        from economy.market import Market
        market_fluct = {}
        if hasattr(self, "market") and self.market:
            market_fluct = dict(self.market._fluctuation)

        return {
            "version": 1,
            "seed": self.seed,
            "rng_state": list(self.rng.getstate()[1]),  # Mersenne Twister state
            "rng_internalstate": self.rng.getstate()[0],
            "turn_count": self.turn_count,
            "heat": self.heat,
            "cash": self.cash,
            "district": self.district,
            "jobs_completed": getattr(self, "jobs_completed", 0),
            "total_kills": getattr(self, "total_kills", 0),
            "controlled_districts": getattr(self, "controlled_districts", []),
            "_last_level": self._last_level,
            "market_fluctuation": market_fluct,
            "player": self.player.to_dict(),
            "crew": self.crew.to_dict(),
            "map": self.game_map.to_dict(),
            "message_log": [
                {"text": m.plain_text, "fg": list(m.fg)}
                for m in self.message_log.messages[-60:]
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Engine":
        """Reconstruct engine from save dict. Does not restore tcod context."""
        from entities.actor import Actor
        from world.game_map import GameMap
        from components.crew_member import CrewRoster
        from entities.character_class import CharacterClass
        from economy.market import Market
        from economy.heat import HeatSystem

        player = Actor.player_from_dict(data["player"])
        char_class = CharacterClass(data["player"]["char_class"])

        game_map = GameMap.from_dict(data["map"], player_entity=player)

        engine = cls(
            player=player,
            game_map=game_map,
            seed=data.get("seed", 0),
            char_class=char_class,
        )

        # Restore RNG state
        internalstate = data.get("rng_internalstate", 3)
        mt_state = tuple(data.get("rng_state", []))
        if mt_state:
            engine.rng.setstate((internalstate, mt_state, None))

        engine.turn_count = data.get("turn_count", 0)
        engine.heat = data.get("heat", 0)
        engine.cash = data.get("cash", 100)
        engine.district = data.get("district", "West Bottoms")
        engine.jobs_completed = data.get("jobs_completed", 0)
        engine.total_kills = data.get("total_kills", 0)
        engine.controlled_districts = data.get("controlled_districts", [])
        engine._last_level = data.get("_last_level", 1)

        engine.crew = CrewRoster.from_dict(data.get("crew", []))
        engine.market = Market(engine.rng)
        engine.market._fluctuation.update(data.get("market_fluctuation", {}))
        engine.heat_system = HeatSystem(engine)

        # Restore message log
        from ui.message_log import Message
        for md in data.get("message_log", []):
            engine.message_log.messages.append(
                Message(md["text"], tuple(md["fg"]))
            )

        engine.update_fov()
        return engine

    def save_game(self, slot: int = 0) -> None:
        from engine.save_load import save_game
        save_game(self, slot)
