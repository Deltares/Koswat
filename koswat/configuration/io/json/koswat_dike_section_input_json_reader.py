"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from pathlib import Path

from koswat.configuration.io.config_sections import (
    CofferdamReinforcementSectionFom,
    DikeProfileSectionFom,
    PipingWallReinforcementSectionFom,
    SoilReinforcementSectionFom,
    StabilitywallReinforcementSectionFom,
    VPSReinforcementSectionFom,
)
from koswat.configuration.io.json.koswat_dike_section_input_json_fom import (
    KoswatDikeSectionInputJsonFom,
)
from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatDikeSectionInputJsonReader(KoswatReaderProtocol):
    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".json"

    def read(self, file_path: Path) -> KoswatDikeSectionInputJsonFom:
        if not self.supports_file(file_path):
            raise ValueError("Json file should be provided")

        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        _json_fom = KoswatJsonReader().read(file_path)
        _dike_section_input_fom = KoswatDikeSectionInputJsonFom(
            dike_section=_json_fom.file_stem,
            input_profile=DikeProfileSectionFom.from_config(
                _json_fom.content.get("dijkprofiel", dict()), set_defaults=False
            ),
            soil_measure=SoilReinforcementSectionFom.from_config(
                _json_fom.content.get("grondmaatregel", dict()), set_defaults=False
            ),
            vps=VPSReinforcementSectionFom.from_config(
                _json_fom.content.get("verticalepipingoplossing", dict()),
                set_defaults=False,
            ),
            piping_wall=PipingWallReinforcementSectionFom.from_config(
                _json_fom.content.get("kwelscherm", dict()), set_defaults=False
            ),
            stability_wall=StabilitywallReinforcementSectionFom.from_config(
                _json_fom.content.get("stabiliteitswand", dict()), set_defaults=False
            ),
            cofferdam=CofferdamReinforcementSectionFom.from_config(
                _json_fom.content.get("kistdam", dict()), set_defaults=False
            ),
        )
        _dike_section_input_fom.input_profile.dike_section = (
            _dike_section_input_fom.dike_section
        )

        return _dike_section_input_fom
