from __future__ import annotations

import math

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


class KoswatScenario(KoswatConfigProtocol):
    scenario_name: str
    scenario_section: str
    d_h: float
    d_s: float
    d_p: float
    kruin_breedte: float
    buiten_talud: float

    def __init__(self) -> None:
        self.scenario_name = ""
        self.scenario_section = ""
        self.d_h = math.nan
        self.d_s = math.nan
        self.d_p = math.nan
        self.kruin_breedte = math.nan
        self.buiten_talud = math.nan

    def is_valid(self) -> bool:
        return (
            not math.isnan(self.d_h)
            and not math.isnan(self.d_s)
            and not math.isnan(self.d_p)
        )

    @classmethod
    def from_dict(cls, scenario_data: dict) -> KoswatScenario:
        _scenario = cls()
        _scenario.scenario_name = scenario_data.get("scenario_name", "")
        _scenario.scenario_section = scenario_data.get("scenario_section", "")
        _scenario.d_h = scenario_data["d_h"]
        _scenario.d_s = scenario_data["d_s"]
        _scenario.d_p = scenario_data["d_p"]
        _scenario.kruin_breedte = scenario_data["kruin_breedte"]
        _scenario.buiten_talud = scenario_data["buiten_talud"]
        return _scenario
