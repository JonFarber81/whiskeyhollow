"""Actor entity — player, NPCs, enemies."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

from entities.entity import Entity, RenderOrder

if TYPE_CHECKING:
    from components.fighter import Fighter
    from components.ai.base_ai import BaseAI
    from components.inventory import Inventory
    from world.game_map import GameMap


class Actor(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "@",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<unnamed>",
        fighter: Optional[Fighter] = None,
        ai: Optional[BaseAI] = None,
        inventory: Optional[Inventory] = None,
        game_map: Optional[GameMap] = None,
    ) -> None:
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
            game_map=game_map,
        )
        self.fighter = fighter
        if self.fighter:
            self.fighter.entity = self

        self.ai = ai
        if self.ai:
            self.ai.entity = self

        self.inventory = inventory
        if self.inventory:
            self.inventory.entity = self

    @property
    def is_alive(self) -> bool:
        return bool(self.fighter and self.fighter.hp > 0)
