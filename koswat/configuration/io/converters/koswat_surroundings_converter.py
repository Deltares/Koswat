import logging
from pathlib import Path
from typing import List

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
    KoswatTrajectSurroundingsWrapperCollectionCsvFom,
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom_builder import (
    KoswatSurroundingsCsvFomBuilder,
)
from koswat.io.csv.koswat_csv_reader import KoswatCsvReader


def from_surroundings_csv_dir_to_fom(
    csv_dir: Path,
) -> KoswatTrajectSurroundingsWrapperCollectionCsvFom:
    if not csv_dir.is_dir():
        logging.error("Surroundings directory not found at {}".format(csv_dir))
        return []
    _collection = KoswatTrajectSurroundingsWrapperCollectionCsvFom()
    for _traject_surrounding in csv_dir.iterdir():
        _surroundings_wrapper = KoswatTrajectSurroundingsWrapperCsvFom()
        _surroundings_wrapper.traject = _traject_surrounding.stem
        _collection.wrapper_collection[
            _traject_surrounding.stem
        ] = _surroundings_wrapper
        for _csv_file in _traject_surrounding.glob("*.csv"):
            _surrounding_type = (
                _csv_file.stem.replace(f"T_{_traject_surrounding.stem}_", "")
                .lower()
                .strip()
            )
            _surrounding_fom = KoswatCsvReader.with_builder_type(
                KoswatSurroundingsCsvFomBuilder
            ).read(_csv_file)
            _surrounding_fom.traject = _traject_surrounding.stem
            _surroundings_wrapper.surroundings[_surrounding_type] = _surrounding_fom
    return _collection


def from_surroundings_csv_file_to_fom(
    csv_file: Path,
) -> KoswatTrajectSurroundingsCsvFom:
    if not csv_file.is_file():
        logging.error("Surroundings file not found at {}".format(csv_file))
        return None
    return KoswatCsvReader.with_builder_type(KoswatSurroundingsCsvFomBuilder).read(
        csv_file
    )
