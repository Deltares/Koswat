from __future__ import annotations

from configparser import ConfigParser
from typing import List, Optional

from koswat.configuration.koswat_scenario import KoswatScenario
from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class SectionScenarioFom(KoswatScenario, KoswatIniFomProtocol):
    scenario_name: str
    scenario_section: str
    d_h: float
    d_s: float
    d_p: float
    # If the following ones are not provided we should use the ones from the original profile
    buiten_talud: Optional[float]
    kruin_breedte: Optional[float]

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> SectionScenarioFom:
        _section = cls()
        # Retrieves the values as written (and expected) in the ini file.
        _section.d_h = ini_config.getfloat("dH")
        _section.d_s = ini_config.getfloat("dS")
        _section.d_p = ini_config.getfloat("dP")
        _section.buiten_talud = ini_config.getfloat("Buitentalud")
        _section.kruin_breedte = ini_config.getfloat("kruinbreedte")
        return _section


class KoswatSectionScenariosIniFom(KoswatIniFomProtocol):
    section_scenarios: List[SectionScenarioFom]

    def __init__(self) -> None:
        self._section_name = ""

    @property
    def section_name(self) -> str:
        return self._section_name

    @section_name.setter
    def section_name(self, value: str) -> None:
        self._section_name = value
        for _scenario in self.section_scenarios:
            _scenario.scenario_section = self._section_name

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _ini_fom = cls()
        _ini_fom.section_scenarios = []
        for _section_name in ini_config.sections():
            _new_section = SectionScenarioFom.from_config(ini_config[_section_name])
            _new_section.scenario_name = _section_name
            _ini_fom.section_scenarios.append(_new_section)
        return _ini_fom
