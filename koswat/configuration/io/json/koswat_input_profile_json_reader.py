from pathlib import Path

from koswat.configuration.io.json.koswat_input_profile_json_fom import (
    KoswatInputProfileJsonFom,
)
from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatInputProfileJsonReader(KoswatReaderProtocol):
    def read(self, file_path: Path) -> KoswatInputProfileJsonFom:
        _json_fom = KoswatJsonReader().read(file_path)

        def _format_headers(csv_entries: list[str]) -> list[str]:
            return list(map(lambda x: x.lower().strip().split(" ")[0], csv_entries))

        _json_fom.headers = _format_headers(_json_fom.headers)
        _koswat_fom = KoswatInputProfileJsonFom()
        _koswat_fom.input_profile_fom_list = []
        for _entry in _json_fom.entries:
            _input_profile = dict(zip(_json_fom.headers, _entry))
            _koswat_fom.input_profile_fom_list.append(_input_profile)
        return _koswat_fom
