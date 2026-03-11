"""Market — per-district contraband prices with fluctuation."""

from __future__ import annotations

import random
from typing import Dict, Tuple

from economy.contraband import CONTRABAND_TYPES


# District demand modifiers (multipliers on base_value)
DISTRICT_MODIFIERS: Dict[str, Dict[str, float]] = {
    "West Bottoms": {
        "whiskey": 0.9, "beer": 1.1, "gin": 0.9, "medicinal_alcohol": 1.0,
    },
    "River Market": {
        "whiskey": 1.0, "beer": 0.9, "gin": 1.1, "medicinal_alcohol": 1.2,
    },
    "18th and Vine": {
        "whiskey": 1.3, "beer": 1.0, "gin": 1.2, "medicinal_alcohol": 0.8,
    },
    "Union Station": {
        "whiskey": 1.1, "beer": 1.3, "gin": 1.0, "medicinal_alcohol": 1.1,
    },
    "Westport": {
        "whiskey": 1.2, "beer": 0.8, "gin": 1.3, "medicinal_alcohol": 0.9,
    },
}


class Market:
    def __init__(self, rng: random.Random) -> None:
        self.rng = rng
        # Current fluctuation multipliers per contraband key
        self._fluctuation: Dict[str, float] = {k: 1.0 for k in CONTRABAND_TYPES}

    def sell_price(self, contraband_key: str, district: str, player=None) -> int:
        """Return current sell price for contraband in the given district."""
        from entities.perks import has_perk
        base = CONTRABAND_TYPES[contraband_key].base_value
        district_mod = DISTRICT_MODIFIERS.get(district, {}).get(contraband_key, 1.0)
        fluct = self._fluctuation.get(contraband_key, 1.0)
        price = max(1, int(base * district_mod * fluct))

        # Phase 15: Jazz District Barfly rank perk — +15% sell price
        if player:
            standing = getattr(player, "faction_standing", None)
            if standing and standing.get_rep("jazz_district") >= 10:
                price = int(price * 1.15)
            # Phase 16: Black Market perk — +15% sell price (stacks)
            if has_perk(player, "black_market"):
                price = int(price * 1.15)

        return max(1, price)

    def fluctuate_prices(self) -> None:
        """Randomize price modifiers each chapter turn."""
        for key in self._fluctuation:
            delta = self.rng.uniform(-0.15, 0.20)
            new_val = self._fluctuation[key] * (1 + delta)
            self._fluctuation[key] = max(0.5, min(2.0, new_val))
