"""Inventory component."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from entities.actor import Actor
    from entities.item import Item


@dataclass
class Inventory:
    capacity: int
    items: List[Item] = field(default_factory=list)
    entity: Optional[Actor] = field(default=None, repr=False)

    @property
    def equipped_weapon(self) -> Optional[Item]:
        from entities.item import ItemType
        for item in self.items:
            if item.item_type == ItemType.WEAPON and getattr(item, "equipped", False):
                return item
        return None

    def add(self, item: Item) -> bool:
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def remove(self, item: Item) -> None:
        self.items.remove(item)
