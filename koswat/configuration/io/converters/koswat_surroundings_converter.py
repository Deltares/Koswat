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


def translate_surrounding_type(surrounding_type: str) -> str:
    _normalized = surrounding_type.lower().strip()
    _translations = dict(
        bebouwing_binnendijks="buldings_polderside",
        bebouwing_buitendijks="buildings_dikeside",
        spoor_binnendijks="platform_polderside",
        spoor_buitendijks="platform_dikeside",
        water_binnendijks="water_polderside",
        water_buitendijks="water_dikeside",
        wegen_binnendijks_klasse2="roads_class_2_polderside",
        wegen_binnendijks_klasse7="roads_class_7_polderside",
        wegen_binnendijks_klasse24="roads_class_24_polderside",
        wegen_binnendijks_klasse47="roads_class_47_polderside",
        wegen_binnendijks_klasse2onbekende="roads_class_unknown_polderside",
        wegen_buitendijks_klasse2="roads_class_2_dikeside",
        wegen_buitendijks_klasse7="roads_class_7_dikeside",
        wegen_buitendijks_klasse24="roads_class_24_dikeside",
        wegen_buitendijks_klasse47="roads_class_47_dikeside",
        wegen_buitendijks_klasse2onbekende="roads_class_unknown_dikeside",
    )
    _translation = _translations.get(_normalized, None)
    if not _translations:
        logging.error("No mapping found for {}".format(surrounding_type))
        return None
    return _translation


# Move this into a koswat_surroundings_importer class
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
            _surrounding_type = translate_surrounding_type(
                _csv_file.stem.replace(f"T_{_traject_surrounding.stem}_", "")
            )
            _surrounding_fom = KoswatCsvReader.with_builder_type(
                KoswatSurroundingsCsvFomBuilder
            ).read(_csv_file)
            _surrounding_fom.traject = _traject_surrounding.stem
            setattr(_surroundings_wrapper, _surrounding_type, _surrounding_fom)
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
