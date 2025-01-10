from pathlib import Path
from typing import List

from koswat.configuration.io.csv.koswat_input_profiles_csv_fom import (
    KoswatInputProfilesCsvFom,
)
from koswat.core.io.csv.koswat_csv_reader import KoswatCsvReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class KoswatInputProfilesCsvReader(KoswatReaderProtocol):
    def read(self, file_path: Path) -> KoswatInputProfilesCsvFom:
        _csv_fom = KoswatCsvReader().read(file_path)

        def _format_headers(csv_entries: List[str]) -> List[str]:
            return list(map(lambda x: x.lower().strip().split(" ")[0], csv_entries))

        _csv_fom.headers = _format_headers(_csv_fom.headers)
        _koswat_fom = KoswatInputProfilesCsvFom()
        _koswat_fom.input_profile_fom_list = []
        for _entry in _csv_fom.entries:
            _input_profile = dict(zip(_csv_fom.headers, _entry))
            _koswat_fom.input_profile_fom_list.append(_input_profile)
        return _koswat_fom
