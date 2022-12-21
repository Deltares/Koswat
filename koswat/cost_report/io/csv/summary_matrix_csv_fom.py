from typing import List

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


class SummaryMatrixCsvFom(KoswatCsvFomProtocol):

    headers: List[str]
    cost_rows: List[List[str]]
    location_rows: List[List[str]]

    def __init__(self) -> None:
        self.headers = []
        self.cost_rows = []
        self.location_rows = []

    def is_valid(self) -> bool:
        if not self.headers:
            return False
        _len_headers = len(self.headers)
        _valid_cost_rows = all(len(_c_row) == _len_headers for _c_row in self.cost_rows)
        _valid_loc_rows = all(
            len(_l_row) == _len_headers for _l_row in self.location_rows
        )
        return _valid_cost_rows and _valid_loc_rows
