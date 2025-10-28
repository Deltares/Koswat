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
                _json_fom.content.get("dijkprofiel", dict())
            ),
            soil_measure=SoilReinforcementSectionFom.from_config(
                _json_fom.content.get("grondmaatregel", dict())
            ),
            vps=VPSReinforcementSectionFom.from_config(
                _json_fom.content.get("verticalepipingoplossing", dict())
            ),
            piping_wall=PipingWallReinforcementSectionFom.from_config(
                _json_fom.content.get("kwelscherm", dict())
            ),
            stability_wall=StabilitywallReinforcementSectionFom.from_config(
                _json_fom.content.get("stabiliteitswand", dict())
            ),
            cofferdam=CofferdamReinforcementSectionFom.from_config(
                _json_fom.content.get("kistdam", dict())
            ),
        )
        _dike_section_input_fom.input_profile.dike_section = (
            _dike_section_input_fom.dike_section
        )

        return _dike_section_input_fom
