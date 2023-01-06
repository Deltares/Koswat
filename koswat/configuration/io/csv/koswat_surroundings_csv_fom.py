from typing import List

from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class KoswatTrajectSurroundingsCsvFom(KoswatCsvFomProtocol):
    points_surroundings_list: List[PointSurroundings]
    distances_list: List[float]
    traject: str

    def __init__(self) -> None:
        self.points_surroundings_list = []
        self.distances_list = []
        self.traject = ""

    def is_valid(self) -> bool:
        return self.points_surroundings_list and any(self.points_surroundings_list)


class KoswatTrajectSurroundingsWrapperCsvFom(KoswatCsvFomProtocol):
    traject: str
    buldings_polderside: KoswatTrajectSurroundingsCsvFom
    buildings_dikeside: KoswatTrajectSurroundingsCsvFom

    platform_polderside: KoswatTrajectSurroundingsCsvFom
    platform_dikeside: KoswatTrajectSurroundingsCsvFom

    water_polderside: KoswatTrajectSurroundingsCsvFom
    water_dikeside: KoswatTrajectSurroundingsCsvFom

    roads_class_2_polderside: KoswatTrajectSurroundingsCsvFom
    roads_class_7_polderside: KoswatTrajectSurroundingsCsvFom
    roads_class_24_polderside: KoswatTrajectSurroundingsCsvFom
    roads_class_47_polderside: KoswatTrajectSurroundingsCsvFom
    roads_class_unknown_polderside: KoswatTrajectSurroundingsCsvFom

    roads_class_2_dikeside: KoswatTrajectSurroundingsCsvFom
    roads_class_7_dikeside: KoswatTrajectSurroundingsCsvFom
    roads_class_24_dikeside: KoswatTrajectSurroundingsCsvFom
    roads_class_47_dikeside: KoswatTrajectSurroundingsCsvFom
    roads_class_unknown_dikeside: KoswatTrajectSurroundingsCsvFom

    def __init__(self) -> None:
        self.traject = ""
        self.buldings_polderside = None
        self.buildings_dikeside = None
        self.platform_polderside = None
        self.platform_dikeside = None
        self.water_polderside = None
        self.water_dikeside = None
        self.roads_class_2_polderside = None
        self.roads_class_7_polderside = None
        self.roads_class_24_polderside = None
        self.roads_class_47_polderside = None
        self.roads_class_unknown_polderside = None
        self.roads_class_2_dikeside = None
        self.roads_class_7_dikeside = None
        self.roads_class_24_dikeside = None
        self.roads_class_47_dikeside = None
        self.roads_class_unknown_dikeside = None

    def is_valid(self) -> bool:
        _surroundings = [
            _prop for _name, _prop in self.__dict__.items() if _name != "traject"
        ]
        return any(_surroundings) and all(_s.is_valid() for _s in _surroundings)
