import logging
from dataclasses import dataclass, field
from pathlib import Path

from koswat.configuration.io.json.koswat_dike_section_input_json_fom import (
    KoswatDikeSectionInputJsonFom,
)
from koswat.configuration.io.json.koswat_dike_section_input_json_reader import (
    KoswatDikeSectionInputJsonReader,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol


@dataclass(kw_only=True)
class KoswatInputProfileListImporter(KoswatImporterProtocol):
    dike_selection: list[str] = field(default_factory=list)

    def import_from(self, from_path: Path) -> list[KoswatDikeSectionInputJsonFom]:
        _files = list(from_path.glob("*.json"))

        _section_input_list = []
        for _section in self.dike_selection if self.dike_selection else []:
            if _section not in (_file.stem for _file in _files):
                logging.error(
                    "The selected dike section %s was not found in the input profile files.",
                    _section,
                )

            _file = from_path.joinpath(f"{_section}.json")
            if not _file.exists():
                continue

            _section_input_list.append(KoswatDikeSectionInputJsonReader().read(_file))

        return _section_input_list
