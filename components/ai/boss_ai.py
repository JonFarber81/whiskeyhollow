"""Boss AI — Phase 13.

Two-phase boss behavior:
  Phase 1 (HP > threshold): Smart chasing + dialog taunts
  Phase 2 (HP <= threshold): Calls reinforcements or goes berserk
"""

from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

from components.ai.base_ai import BaseAI

if TYPE_CHECKING:
    from engine.engine import Engine


class BossAI(BaseAI):
    def __init__(
        self,
        npc_key: str,
        phase_threshold: float = 0.5,
        phase_two_behavior: str = "calls_reinforcements",
    ) -> None:
        self.npc_key = npc_key
        self.phase_threshold = phase_threshold
        self.phase_two_behavior = phase_two_behavior
        self.phase = 1
        self.path: List[Tuple[int, int]] = []
        self._taunt_turns: int = 0
        self._phase_two_triggered: bool = False

    def perform(self, engine: Engine) -> None:
        fighter = self.entity.fighter
        if not fighter or fighter.hp <= 0:
            return

        hp_pct = fighter.hp / fighter.max_hp
        player = engine.player

        # Check phase transition
        if hp_pct <= self.phase_threshold and not self._phase_two_triggered:
            self._enter_phase_two(engine)

        # Only act if player is visible on map
        if not engine.game_map.visible[self.entity.x, self.entity.y]:
            self._wander(engine)
            return

        # Trigger on-attack or on-low-hp dialog
        if self.phase == 2 and self._taunt_turns % 5 == 0:
            self._say_dialog(engine, "on_low_hp" if hp_pct < 0.25 else "on_attack")
        self._taunt_turns += 1

        # Chase and attack
        dx = player.x - self.entity.x
        dy = player.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if distance <= 1:
            from combat.combat_engine import resolve_attack
            resolve_attack(self.entity, player, engine)
        else:
            if not self.path:
                self.path = self.get_path_to(player.x, player.y, engine)
            if self.path:
                dest_x, dest_y = self.path.pop(0)
                blocking = engine.game_map.get_blocking_entity_at(dest_x, dest_y)
                if not blocking or blocking is player:
                    self.entity.move(dest_x - self.entity.x, dest_y - self.entity.y)
                    self.path = []  # Recalc next turn

    def _enter_phase_two(self, engine: Engine) -> None:
        from ui import color as Color
        self._phase_two_triggered = True
        self.phase = 2

        self._say_dialog(engine, "on_low_hp")

        if self.phase_two_behavior == "calls_reinforcements":
            self._spawn_reinforcements(engine)
        elif self.phase_two_behavior == "berserk":
            # Berserk: +2 attack, ignore defense
            if self.entity.fighter:
                self.entity.fighter.base_attack += 2
            engine.message_log.add_message(
                f"{self.entity.name} goes BERSERK!", fg=Color.RED
            )

    def _spawn_reinforcements(self, engine: Engine) -> None:
        from ui import color as Color
        from entities.actor import Actor
        from components.fighter import Fighter
        from components.ai.hostile_ai import HostileEnemy

        spawned = 0
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = self.entity.x + dx, self.entity.y + dy
            if (engine.game_map.in_bounds(nx, ny)
                    and engine.game_map.tiles["walkable"][nx, ny]
                    and not engine.game_map.get_blocking_entity_at(nx, ny)):
                goon = Actor(
                    x=nx, y=ny,
                    char="g", color=(180, 80, 40),
                    name="Rival Goon",
                    fighter=Fighter(max_hp=20, hp=20, base_attack=3, base_defense=1),
                    ai=HostileEnemy(),
                    game_map=engine.game_map,
                )
                spawned += 1
                if spawned >= 2:
                    break

        if spawned > 0:
            engine.message_log.add_message(
                f"{self.entity.name} calls for backup! {spawned} goon(s) appear!",
                fg=Color.ORANGE,
            )

    def _wander(self, engine: Engine) -> None:
        """Random walk when player isn't visible."""
        import random
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        engine.rng.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = self.entity.x + dx, self.entity.y + dy
            if (engine.game_map.in_bounds(nx, ny)
                    and engine.game_map.tiles["walkable"][nx, ny]
                    and not engine.game_map.get_blocking_entity_at(nx, ny)):
                self.entity.move(dx, dy)
                break

    def _say_dialog(self, engine: Engine, event_type: str) -> None:
        """Show a dialog line from the NPC's dialogue dict."""
        from ui import color as Color
        try:
            import json, os
            path = os.path.join(
                os.path.dirname(__file__), "..", "..", "data", "npcs.json"
            )
            with open(path) as f:
                npcs = json.load(f)
            npc_data = npcs.get(self.npc_key, {})
            lines = npc_data.get("dialogue", {}).get(event_type, [])
            if lines:
                line = engine.rng.choice(lines)
                engine.message_log.add_message(
                    f'{self.entity.name}: "{line}"', fg=Color.GOLD
                )
        except Exception:
            pass  # Never crash on dialog
