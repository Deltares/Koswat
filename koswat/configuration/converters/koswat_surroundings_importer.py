import logging
from pathlib import Path
from typing import Any, List, Tuple

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
    KoswatTrajectSurroundingsWrapperCollectionCsvFom,
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom_builder import (
    KoswatSurroundingsCsvFomBuilder,
)
from koswat.io.csv.koswat_csv_reader import KoswatCsvReader


class KoswatSurroundingsImporter(BuilderProtocol):
    surroundings_csv_dir: Path

    def __init__(self) -> None:
        self.surroundings_csv_dir = None

    def _map_surrounding_type(self, surrounding_type: str) -> str:
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
            wegen_binnendijks_klasseonbekend="roads_class_unknown_polderside",
            wegen_buitendijks_klasse2="roads_class_2_dikeside",
            wegen_buitendijks_klasse7="roads_class_7_dikeside",
            wegen_buitendijks_klasse24="roads_class_24_dikeside",
            wegen_buitendijks_klasse47="roads_class_47_dikeside",
            wegen_buitendijks_klasseonbekend="roads_class_unknown_dikeside",
        )
        _translation = _translations.get(_normalized, None)
        if not _translations:
            logging.error("No mapping found for {}".format(surrounding_type))
            return None
        return _translation

    def _csv_file_to_fom(
        self, csv_file: Path, traject_name: str
    ) -> Tuple[str, KoswatTrajectSurroundingsCsvFom]:
        _surrounding_csv_fom = KoswatCsvReader.with_builder_type(
            KoswatSurroundingsCsvFomBuilder
        ).read(csv_file)
        _surrounding_csv_fom.traject = traject_name
        _surrounding_type = self._map_surrounding_type(
            _surrounding_csv_fom.stem.replace(f"T_{traject_name}_", "")
        )
        return _surrounding_type, _surrounding_csv_fom

    def _csv_dir_to_fom(
        self,
        csv_dir: Path,
    ) -> Tuple[str, KoswatTrajectSurroundingsWrapperCsvFom]:
        _surroundings_wrapper = KoswatTrajectSurroundingsWrapperCsvFom()
        _surroundings_wrapper.traject = csv_dir.stem
        for _csv_file in csv_dir.glob("*.csv"):
            _type, _csv_fom = self._csv_file_to_fom(_csv_file, csv_dir.stem)
            setattr(_surroundings_wrapper, _type, _csv_fom)
        return (csv_dir.stem, _surroundings_wrapper)

    def build(self) -> Any:
        if not isinstance(self.surroundings_csv_dir, Path):
            raise ValueError("No surroundings csv directory path given.")
        _collection = KoswatTrajectSurroundingsWrapperCollectionCsvFom()
        _collection.wrapper_collection = dict(
            map(self._csv_dir_to_fom, self.surroundings_csv_dir.iterdir())
        )

        return _collection
