from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


class KoswatCsvMultiHeaderFom(KoswatCsvFomProtocol):
    headers: list[list[str]]
    entries: list[list[str]]

    def __init__(self) -> None:
        self.headers = []
        self.entries = []

    def is_valid(self) -> bool:
        if not self.headers or not self.entries:
            return False
        _l_header = max(map(len, self.headers))

        # At the moment, not all rows have the same length
        return all(map(lambda x: len(x) >= _l_header, self.entries))