from __future__ import annotations

from typing import List, Protocol, runtime_checkable

from koswat.builder_protocol import BuilderProtocol
from koswat.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


@runtime_checkable
class KoswatCsvFomBuilderProtocol(BuilderProtocol, Protocol):
    headers: List[str]
    entries: List[List[str]]

    def build(self) -> KoswatCsvFomProtocol:
        pass

    @classmethod
    def from_text(cls, csv_entries: List[List[str]]) -> KoswatCsvFomBuilderProtocol:
        """
        Generates a valid instance of a `KoswatCsvFomBuilderProtocol` based on the provided `csv_text`.

        Args:
            csv_entries (str): Text extracted from a csv file with its entries separated by column and line.

        Returns:
            KoswatCsvFomBuilderProtocol: Valid instance of a `KoswatCsvFomBuilderProtocol`
        """
        pass
