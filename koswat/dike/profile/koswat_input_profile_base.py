from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


@dataclass
class KoswatInputProfileBase(KoswatInputProfileProtocol):
    dike_section: str = ""
    waterside_ground_level: float = math.nan
    waterside_slope: float = math.nan
    waterside_berm_height: float = math.nan
    waterside_berm_width: float = math.nan
    crest_height: float = math.nan
    crest_width: float = math.nan
    polderside_ground_level: float = math.nan
    polderside_slope: float = math.nan
    polderside_berm_height: float = math.nan
    polderside_berm_width: float = math.nan
    ground_price_builtup: float = math.nan
    ground_price_unbuilt: float = math.nan
    factor_settlement: float = math.nan
    pleistocene: float = math.nan
    aquifer: float = math.nan
    thickness_cover_layer: float = math.nan
    thickness_grass_layer: float = math.nan
    thickness_clay_layer: float = math.nan

    @property
    def ground_price(self) -> float:
        return self.ground_price_builtup

    def set_defaults(self, other: "KoswatInputProfileBase") -> "KoswatInputProfileBase":
        """
        Add the defaults from another KoswatInputProfileBase instance to this instance, if not set.

        Args:
            other (KoswatInputProfileBase): The other instance to get defaults from.

        Raises:
            TypeError: If the other instance has a different type.

        Returns:
            KoswatInputProfileBase: The instance with defaults set.
        """
        if not isinstance(other, KoswatInputProfileBase):
            raise TypeError(
                "Can only merge with another KoswatInputProfileBase instance."
            )

        def _set_default(this_value: Any, other_value: Any) -> Any:
            if this_value is None:
                return other_value
            return this_value

        self.dike_section = _set_default(self.dike_section, other.dike_section)
        self.waterside_ground_level = _set_default(
            self.waterside_ground_level, other.waterside_ground_level
        )
        self.waterside_slope = _set_default(self.waterside_slope, other.waterside_slope)
        self.waterside_berm_height = _set_default(
            self.waterside_berm_height, other.waterside_berm_height
        )
        self.waterside_berm_width = _set_default(
            self.waterside_berm_width, other.waterside_berm_width
        )
        self.crest_height = _set_default(self.crest_height, other.crest_height)
        self.crest_width = _set_default(self.crest_width, other.crest_width)
        self.polderside_ground_level = _set_default(
            self.polderside_ground_level, other.polderside_ground_level
        )
        self.polderside_slope = _set_default(
            self.polderside_slope, other.polderside_slope
        )
        self.polderside_berm_height = _set_default(
            self.polderside_berm_height, other.polderside_berm_height
        )
        self.polderside_berm_width = _set_default(
            self.polderside_berm_width, other.polderside_berm_width
        )
        self.ground_price_builtup = _set_default(
            self.ground_price_builtup, other.ground_price_builtup
        )
        self.ground_price_unbuilt = _set_default(
            self.ground_price_unbuilt, other.ground_price_unbuilt
        )
        self.factor_settlement = _set_default(
            self.factor_settlement, other.factor_settlement
        )
        self.pleistocene = _set_default(self.pleistocene, other.pleistocene)
        self.aquifer = _set_default(self.aquifer, other.aquifer)
        self.thickness_cover_layer = _set_default(
            self.thickness_cover_layer, other.thickness_cover_layer
        )
        self.thickness_grass_layer = _set_default(
            self.thickness_grass_layer, other.thickness_grass_layer
        )
        self.thickness_clay_layer = _set_default(
            self.thickness_clay_layer, other.thickness_clay_layer
        )

        return self
