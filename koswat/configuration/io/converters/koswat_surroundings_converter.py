import logging
from pathlib import Path
from typing import List

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom_builder import (
    KoswatSurroundingsCsvFomBuilder,
)
from koswat.io.csv.koswat_csv_reader import KoswatCsvReader


def from_surroundings_csv_dir_to_fom(
    csv_dir: Path,
) -> List[KoswatSurroundingsCsvFom]:
    if not csv_dir.is_dir():
        logging.error("Surroundings directory not found at {}".format(csv_dir))
        return []
    _surroundings_fom = []
    for _traject_surrounding in csv_dir.iterdir():
        _surroundings_csv = (
            _traject_surrounding
            / f"T_{_traject_surrounding.stem}_bebouwing_binnendijks.csv"
        )  # For the MVP we only read one.
        if not _surroundings_csv.is_file():
            logging.warning(
                "Surroundings database file not found for traject {}".format(
                    _traject_surrounding.stem
                )
            )
        _surrounding_fom: KoswatSurroundingsCsvFom = KoswatCsvReader.with_builder_type(
            KoswatSurroundingsCsvFomBuilder
        ).read(_surroundings_csv)
        _surrounding_fom.name = _traject_surrounding.stem
        _surroundings_fom.append(_surrounding_fom)
    return _surrounding_fom
