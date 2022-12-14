from typing import Dict, List, Optional

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


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
    surroundings: Dict[str, KoswatTrajectSurroundingsCsvFom]

    def __init__(self) -> None:
        self.traject = ""
        self.surroundings = {}

    def is_valid(self) -> bool:
        return any(self.surroundings) and all(_s.is_valid() for _s in self.surroundings)


class KoswatTrajectSurroundingsWrapperCollectionCsvFom(KoswatCsvFomProtocol):
    wrapper_collection: Dict[str, KoswatTrajectSurroundingsWrapperCsvFom]

    def __init__(self) -> None:
        self.wrapper_collection = {}

    def get_wrapper_by_traject(
        self, traject: str
    ) -> Optional[KoswatTrajectSurroundingsWrapperCsvFom]:
        return self.wrapper_collection.get(traject, None)
