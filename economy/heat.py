"""Police heat system — tracks wanted level 0-100."""

from __future__ import annotations

from typing import TYPE_CHECKING

from constants import HEAT_COP_PATROL, HEAT_RAID
from ui import color as Color

if TYPE_CHECKING:
    from engine.engine import Engine


class HeatSystem:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def increase(self, amount: int, reason: str = "") -> None:
        """Raise heat, clamped to 100. Trigger events at thresholds."""
        old = self.engine.heat
        self.engine.heat = min(100, self.engine.heat + amount)
        new = self.engine.heat

        if reason:
            self.engine.message_log.add_message(
                f"Heat +{amount}{f' ({reason})' if reason else ''}",
                fg=Color.HEAT_HOT if new >= 66 else Color.HEAT_WARM,
            )

        # Threshold crossings
        if old < HEAT_COP_PATROL <= new:
            self.engine.message_log.add_message(
                "The bulls are on patrol — watch yourself.",
                fg=Color.ORANGE,
            )
        if old < HEAT_RAID <= new:
            self.engine.message_log.add_message(
                "RAID! The feds are moving in!",
                fg=Color.RED,
            )

    def decrease(self, amount: int) -> None:
        """Lower heat (laying low, bribes, etc.)."""
        self.engine.heat = max(0, self.engine.heat - amount)

    def passive_decay(self) -> None:
        """Called each chapter end — heat drops naturally over time."""
        # INT modifier speeds up decay
        stats = getattr(self.engine.player, "stats", None)
        decay = 3 + (stats.int_mod if stats else 0)
        self.engine.heat = max(0, self.engine.heat - decay)
