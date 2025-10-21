import json
from pathlib import Path

from koswat.core.io.json.koswat_json_fom import KoswatJsonFom
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatJsonReader(KoswatReaderProtocol):
    separator: str = ";"

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".json"

    def read(self, file_path: Path) -> KoswatJsonFom:
        if not self.supports_file(file_path):
            raise ValueError("Json file should be provided")

        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        with open(file_path, "r", encoding="utf-8") as _file:
            _json_content = json.load(_file)

        return KoswatJsonFom(file_stem=file_path.stem, content=_json_content)
