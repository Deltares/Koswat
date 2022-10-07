from pathlib import Path

from koswat.io.koswat_csv_fom import KoswatCsvFom, KoswatCsvFomBuilder
from koswat.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatCsvReader(KoswatReaderProtocol):
    separator: str = ";"

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".csv"

    def read(self, file_path: Path) -> KoswatCsvFom:
        if not self.supports_file(file_path):
            raise ValueError("Csv file should be provided")

        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        _csv_lines = file_path.read_text().splitlines(keepends=False)
        entries = [_line.split(self.separator) for _line in _csv_lines]
        _csv_fom_builder = KoswatCsvFomBuilder()
        _csv_fom_builder.headers = entries.pop(0)
        _csv_fom_builder.entries = entries
        return _csv_fom_builder.build()
