from __future__ import annotations
from dataclasses import dataclass

import math

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


@dataclass
class KoswatScenario(KoswatConfigProtocol):
    scenario_name: str = ""
    scenario_section: str = ""
    d_h: float = math.nan
    d_s: float = math.nan
    d_p: float = math.nan
    kruin_breedte: float = math.nan
    buiten_talud: float = math.nan

    def is_valid(self) -> bool:
        return (
            not math.isnan(self.d_h)
            and not math.isnan(self.d_s)
            and not math.isnan(self.d_p)
        )
