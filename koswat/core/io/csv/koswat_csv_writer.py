from pathlib import Path
from typing import List

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.core.io.koswat_writer_protocol import KoswatWriterProtocol


class KoswatCsvWriter(KoswatWriterProtocol):
    separator: str = ";"

    def write(self, fom_instance: KoswatCsvFomProtocol, to_path: Path) -> None:
        if not isinstance(fom_instance, KoswatCsvFomProtocol):
            raise ValueError("Expected instance of type 'KoswatCsvFomProtocol'.")
        if not isinstance(to_path, Path):
            raise ValueError("No write path location provided.")

        def format_line(line: List[str]) -> str:
            return ";".join(map(str, line))

        _lines = list(map(format_line, [fom_instance.headers] + fom_instance.entries))
        _text = "\n".join(_lines)

        to_path.write_text(_text, encoding="utf-8")
