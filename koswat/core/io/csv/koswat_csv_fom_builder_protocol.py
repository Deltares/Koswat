from __future__ import annotations

from typing import List, Protocol, runtime_checkable

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.core.protocols import BuilderProtocol


@runtime_checkable
class KoswatCsvFomBuilderProtocol(BuilderProtocol, Protocol):
    headers: List[str]
    entries: List[List[str]]

    def build(self) -> KoswatCsvFomProtocol:
        """
        Builds a valid instance of a `KoswatCsvFomProtocol` with the provided `headers` and `entries`.

        Returns:
            KoswatCsvFomProtocol: Valid instance representing a Koswat csv file.
        """
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
