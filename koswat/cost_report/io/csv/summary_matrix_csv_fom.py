from typing import List

from koswat.io.file_object_model_protocol import FileObjectModelProtocol


class SummaryMatrixCsvFom(FileObjectModelProtocol):

    headers: List[str]
    cost_rows: List[str]
    location_rows: List[str]

    def __init__(self) -> None:
        self.headers = []
        self.cost_rows = []
        self.location_rows = []

    def is_valid(self) -> bool:
        return any(self.headers) and len(self.headers) == len(self.headers) == len(
            self.location_rows
        )
