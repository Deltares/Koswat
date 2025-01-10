from __future__ import annotations

import math
from dataclasses import dataclass

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

    @property
    def ground_price(self) -> float:
        return self.ground_price_builtup
