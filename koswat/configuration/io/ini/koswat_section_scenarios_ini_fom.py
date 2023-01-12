from __future__ import annotations

from configparser import ConfigParser
from typing import List, Optional

from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class SectionScenarioFom(KoswatIniFomProtocol):
    scenario_name: str
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
        _section.scenario_name = ""
        _section.d_h = ini_config.getfloat("dH")
        _section.d_s = ini_config.getfloat("dS")
        _section.d_p = ini_config.getfloat("dP")
        _section.buiten_talud = ini_config.getfloat("Buitentalud")
        _section.kruin_breedte = ini_config.getfloat("kruinbreedte")
        return _section


class KoswatSectionScenariosIniFom(KoswatIniFomProtocol):
    section_scenarios: List[SectionScenarioFom]
    scenario_dike_section: str

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatSectionScenariosIniFom:
        _ini_fom = cls()
        _ini_fom.section_scenarios = []
        _ini_fom.scenario_dike_section = ""
        for _section_name in ini_config.sections():
            _new_section = SectionScenarioFom.from_config(ini_config[_section_name])
            _new_section.scenario_name = _section_name
            _ini_fom.section_scenarios.append(_new_section)
        return _ini_fom
