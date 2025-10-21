from pathlib import Path
from typing import Any

from koswat.configuration.io.json.koswat_input_profile_json_fom import (
    KoswatInputProfileJsonFom,
)
from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatInputProfileJsonReader(KoswatReaderProtocol):
    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix == ".json"

    def read(self, file_path: Path) -> KoswatInputProfileJsonFom:
        if not self.supports_file(file_path):
            raise ValueError("Json file should be provided")

        if not file_path.is_file():
            raise FileNotFoundError(file_path)

        _json_fom = KoswatJsonReader().read(file_path)

        def _format_headers(input_dict: dict[str, Any]) -> dict[str, Any]:
            return {key.lower(): value for key, value in input_dict.items()}

        return KoswatInputProfileJsonFom(
            input_profile_fom={"dijksectie": _json_fom.file_stem}
            | _format_headers(_json_fom.content["Dijkprofiel"])
        )
