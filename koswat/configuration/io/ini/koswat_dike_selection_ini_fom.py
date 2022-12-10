from __future__ import annotations

from configparser import ConfigParser
from typing import List

from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class DijksectiesSection(KoswatIniFomProtocol):
    dike_sections: List[str]

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatIniFomProtocol:
        _section = cls()
        _section.dike_sections = []
        for _dike_section in ini_config.values():
            _section.dike_sections.append(_dike_section)
        return _section


class KoswatDikeSelectionIniFom(KoswatIniFomProtocol):
    dijksecties_section: DijksectiesSection

    @classmethod
    def from_config(cls, ini_config: ConfigParser) -> KoswatDikeSelectionIniFom:
        _ini_fom = cls()
        _ini_fom.dijksecties_section = DijksectiesSection.from_config(
            ini_config["Dijksecties"]
        )
        return _ini_fom
