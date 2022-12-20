from typing import List

from koswat.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


class KoswatInputProfilesCsvFom(KoswatCsvFomProtocol):
    input_profile_fom_list: List[dict]

    def __init__(self) -> None:
        self.input_profile_fom_list = []

    def is_valid(self) -> bool:
        return self.input_profile_fom_list and any(self.input_profile_fom_list)
