from __future__ import annotations

import math
from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


@dataclass
class KoswatScenario(KoswatConfigProtocol):
    d_h: float
    d_s: float
    d_p: float
    scenario_name: str = ""
    scenario_section: str = ""
    kruin_breedte: float = math.nan
    buiten_talud: float = math.nan

    def is_valid(self) -> bool:
        return (
            not math.isnan(self.d_h)
            and not math.isnan(self.d_s)
            and not math.isnan(self.d_p)
        )
