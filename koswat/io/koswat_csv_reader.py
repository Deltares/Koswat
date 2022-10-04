from pathlib import Path
from typing import List

from koswat.io.koswat_reader_protocol import (
    FileObjectModelProtocol,
    KoswatReaderProtocol,
)


class KoswatCsvFom(FileObjectModelProtocol):
    headers: List[str] = []
    entries: List[List[str]] = []

    def is_valid(self) -> bool:
        if not self.headers or not self.entries:
            return False
        _l_header = len(self.headers)
        return all(map(lambda x: len(x) == _l_header, self.entries))


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
        _csv_form = KoswatCsvFom()
        _csv_form.headers = entries.pop(0)
        _csv_form.entries = entries
        return _csv_form
