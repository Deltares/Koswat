from dataclasses import dataclass

from koswat.configuration.io.csv.koswat_traject_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


@dataclass
class KoswatSurroundingsWrapperCsvFom(KoswatCsvFomProtocol):
    traject: str = ""
    buildings_polderside: KoswatSurroundingsCsvFom = None
    buildings_dikeside: KoswatSurroundingsCsvFom = None

    railways_polderside: KoswatSurroundingsCsvFom = None
    railways_dikeside: KoswatSurroundingsCsvFom = None

    waters_polderside: KoswatSurroundingsCsvFom = None
    waters_dikeside: KoswatSurroundingsCsvFom = None

    roads_class_2_polderside: KoswatSurroundingsCsvFom = None
    roads_class_7_polderside: KoswatSurroundingsCsvFom = None
    roads_class_24_polderside: KoswatSurroundingsCsvFom = None
    roads_class_47_polderside: KoswatSurroundingsCsvFom = None
    roads_class_unknown_polderside: KoswatSurroundingsCsvFom = None

    roads_class_2_dikeside: KoswatSurroundingsCsvFom = None
    roads_class_7_dikeside: KoswatSurroundingsCsvFom = None
    roads_class_24_dikeside: KoswatSurroundingsCsvFom = None
    roads_class_47_dikeside: KoswatSurroundingsCsvFom = None
    roads_class_unknown_dikeside: KoswatSurroundingsCsvFom = None

    def is_valid(self) -> bool:
        _surroundings = [
            _prop for _name, _prop in self.__dict__.items() if _name != "traject"
        ]
        return any(_surroundings) and all(_s.is_valid() for _s in _surroundings)
