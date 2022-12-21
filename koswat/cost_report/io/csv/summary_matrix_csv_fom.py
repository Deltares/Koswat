from typing import List

from koswat.core.io.file_object_model_protocol import ExportFileObjectModelProtocol


class SummaryMatrixCsvFom(ExportFileObjectModelProtocol):

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

    def get_lines(self) -> List[str]:
        def format_line(line: List[str]) -> str:
            return ";".join(map(str, line))

        _lines = [self.headers]
        _lines.extend(self.cost_rows)
        _lines.extend(self.location_rows)

        return list(map(format_line, _lines))
