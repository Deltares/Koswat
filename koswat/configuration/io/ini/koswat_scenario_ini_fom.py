from __future__ import annotations

from configparser import ConfigParser
from typing import List, Optional

from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class ScenarioSection(KoswatIniFomProtocol):
    scenario_name: str
    dH: float
    dS: float
    dP: float
    buitentalud: Optional[float]
    kruinbreedte: Optional[float]

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> ScenarioSection:
        _section = cls()

        _section.scenario_name = ini_config.name
        _section.dH = ini_config.getfloat("dH")
        _section.dS = ini_config.getfloat("dS")
        _section.dP = ini_config.getfloat("dP")
        _section.buitentalud = ini_config.getfloat("Buitentalud")
        _section.kruinbreedte = ini_config.getfloat("kruinbreedte")
        return _section


class KoswatScenarioIniFom(KoswatIniFomProtocol):
    scenario_sections: List[ScenarioSection]

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _ini_fom = cls()
        _ini_fom.scenario_sections = []
        for _section_name in ini_config.sections():
            _new_section = ScenarioSection.from_config(ini_config[_section_name])
            _ini_fom.scenario_sections.append(_new_section)
        return _ini_fom
