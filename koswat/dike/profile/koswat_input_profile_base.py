from __future__ import annotations

import math
from dataclasses import dataclass

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


@dataclass
class KoswatInputProfileBase(KoswatInputProfileProtocol):
    dike_section: str = ""
    buiten_maaiveld: float = math.nan
    buiten_talud: float = math.nan
    buiten_berm_hoogte: float = math.nan
    buiten_berm_breedte: float = math.nan
    kruin_hoogte: float = math.nan
    kruin_breedte: float = math.nan
    binnen_talud: float = math.nan
    binnen_berm_hoogte: float = math.nan
    binnen_berm_breedte: float = math.nan
    binnen_maaiveld: float = math.nan
    pleistoceen: float = math.nan
    aquifer: float = math.nan
