from pathlib import Path
from typing import Type

from koswat.io.csv.koswat_csv_fom_builder_protocol import KoswatCsvFomBuilderProtocol
from koswat.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatCsvReader(KoswatReaderProtocol):
    separator: str = ";"
    koswat_csv_fom_builder_type: Type[KoswatCsvFomBuilderProtocol]

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".csv"

    def read(self, file_path: Path) -> KoswatCsvFomProtocol:
        if not self.supports_file(file_path):
            raise ValueError("Csv file should be provided")

        if not self.koswat_csv_fom_type:
            raise ValueError("Csv FOM builder type needs to be specified")

        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        _csv_lines = file_path.read_text().splitlines(keepends=False)
        _csv_entries = [_line.split(self.separator) for _line in _csv_lines]
        return self.koswat_csv_fom_builder_type.from_text(_csv_entries).build()
