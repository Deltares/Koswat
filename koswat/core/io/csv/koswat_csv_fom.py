from typing import List

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


class KoswatCsvFom(KoswatCsvFomProtocol):
    headers: List[str]
    entries: List[List[str]]

    def __init__(self) -> None:
        self.headers = []
        self.entries = []

    def is_valid(self) -> bool:
        if not self.headers or not self.entries:
            return False
        _l_header = len(self.headers)
        return all(map(lambda x: len(x) == _l_header, self.entries))
