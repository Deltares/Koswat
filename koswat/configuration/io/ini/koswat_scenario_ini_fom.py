from __future__ import annotations

from configparser import ConfigParser
from typing import List, Optional

from koswat.configuration.koswat_scenario import KoswatScenario
from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class ScenarioSection(KoswatScenario, KoswatIniFomProtocol):
    scenario_name: str
    d_h: float
    d_s: float
    d_p: float
    buiten_talud: Optional[float]
    kruin_breedte: Optional[float]

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> ScenarioSection:
        _section = cls()
        # Retrieves the values as written (and expected) in the ini file.
        _section.d_h = ini_config.getfloat("dH")
        _section.d_s = ini_config.getfloat("dS")
        _section.d_p = ini_config.getfloat("dP")
        _section.buiten_talud = ini_config.getfloat("Buitentalud")
        _section.kruin_breedte = ini_config.getfloat("kruinbreedte")
        return _section


class KoswatScenarioIniFom(KoswatIniFomProtocol):
    scenario_sections: List[ScenarioSection]
    scenario_name: str

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _ini_fom = cls()
        _ini_fom.scenario_sections = []
        for _section_name in ini_config.sections():
            _new_section = ScenarioSection.from_config(ini_config[_section_name])
            _new_section.scenario_name = _section_name
            _ini_fom.scenario_sections.append(_new_section)
        return _ini_fom
