from typing import List

from koswat.configuration.io.csv.koswat_input_profiles_csv_fom import (
    KoswatInputProfilesCsvFom,
)
from koswat.core.io.csv.koswat_csv_fom_builder_protocol import (
    KoswatCsvFomBuilderProtocol,
)


class KoswatProfileInputCsvFomBuilder(KoswatCsvFomBuilderProtocol):
    headers: List[str]
    entries: List[List[str]]

    def __init__(self) -> None:
        self.headers = []
        self.entries = []

    def _is_valid(self) -> bool:
        if not self.headers or not self.entries:
            return False
        _l_header = len(self.headers)
        return all(map(lambda x: len(x) == _l_header, self.entries))

    def build(self) -> KoswatInputProfilesCsvFom:
        if not self._is_valid():
            raise ValueError("Not valid headers and entries combination.")
        # First three columns are section x and y coordinate.
        _koswat_fom = KoswatInputProfilesCsvFom()
        _koswat_fom.input_profile_fom_list = []
        for _entry in self.entries:
            _input_profile = dict(zip(self.headers, _entry))
            _koswat_fom.input_profile_fom_list.append(_input_profile)
        return _koswat_fom

    @classmethod
    def from_text(cls, csv_entries: List[List[str]]) -> KoswatCsvFomBuilderProtocol:
        _builder = cls()

        def _fromat_headers(csv_entries: List[str]) -> List[str]:
            return list(map(lambda x: x.lower().strip().split(" ")[0], csv_entries))

        _builder.headers = _fromat_headers(csv_entries.pop(0))
        _builder.entries = csv_entries
        return _builder
