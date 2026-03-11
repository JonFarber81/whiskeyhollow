"""Item entity — weapons, contraband, cash, evidence."""

from __future__ import annotations

from enum import auto, Enum
from typing import Optional, Tuple

from entities.entity import Entity, RenderOrder


class ItemType(Enum):
    WEAPON = auto()
    CONTRABAND = auto()
    CASH = auto()
    EVIDENCE = auto()
    CONSUMABLE = auto()


class Item(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "!",
        color: Tuple[int, int, int] = (180, 200, 80),
        name: str = "<item>",
        item_type: ItemType = ItemType.CONSUMABLE,
        description: str = "",
    ) -> None:
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )
        self.item_type = item_type
        self.description = description
