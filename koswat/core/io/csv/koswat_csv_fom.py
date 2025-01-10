from dataclasses import dataclass, field

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


@dataclass
class KoswatCsvFom(KoswatCsvFomProtocol):
    headers: list[str] = field(default_factory=list)
    entries: list[list[str]] = field(default_factory=list)

    def is_valid(self) -> bool:
        if not self.headers or not self.entries:
            return False
        _l_header = len(self.headers)

        # At the moment, not all rows have the same length
        return all(map(lambda x: len(x) >= _l_header, self.entries))
