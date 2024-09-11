from dataclasses import dataclass

from koswat.configuration.io.csv.koswat_traject_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
)
from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


@dataclass
class KoswatTrajectSurroundingsWrapperCsvFom(KoswatCsvFomProtocol):
    traject: str = ""
    buildings_polderside: KoswatTrajectSurroundingsCsvFom = None
    buildings_dikeside: KoswatTrajectSurroundingsCsvFom = None

    railways_polderside: KoswatTrajectSurroundingsCsvFom = None
    railways_dikeside: KoswatTrajectSurroundingsCsvFom = None

    waters_polderside: KoswatTrajectSurroundingsCsvFom = None
    waters_dikeside: KoswatTrajectSurroundingsCsvFom = None

    roads_class_2_polderside: KoswatTrajectSurroundingsCsvFom = None
    roads_class_7_polderside: KoswatTrajectSurroundingsCsvFom = None
    roads_class_24_polderside: KoswatTrajectSurroundingsCsvFom = None
    roads_class_47_polderside: KoswatTrajectSurroundingsCsvFom = None
    roads_class_unknown_polderside: KoswatTrajectSurroundingsCsvFom = None

    roads_class_2_dikeside: KoswatTrajectSurroundingsCsvFom = None
    roads_class_7_dikeside: KoswatTrajectSurroundingsCsvFom = None
    roads_class_24_dikeside: KoswatTrajectSurroundingsCsvFom = None
    roads_class_47_dikeside: KoswatTrajectSurroundingsCsvFom = None
    roads_class_unknown_dikeside: KoswatTrajectSurroundingsCsvFom = None

    def is_valid(self) -> bool:
        _surroundings = [
            _prop for _name, _prop in self.__dict__.items() if _name != "traject"
        ]
        return any(_surroundings) and all(_s.is_valid() for _s in _surroundings)
