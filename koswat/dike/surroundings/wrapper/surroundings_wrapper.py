from shapely.geometry import Point

from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
)
from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.railways_polderside.koswat_railways_polderside import (
    KoswatRailwaysPolderside,
)
from koswat.dike.surroundings.waters_polderside.koswat_waters_polderside import (
    KoswatWatersPolderside,
)


class SurroundingsWrapper:
    dike_section: str
    traject: str
    subtraject: str

    buildings_polderside: KoswatBuildingsPolderside
    buildings_dikeside: KoswatSurroundingsProtocol

    railways_polderside: KoswatRailwaysPolderside
    railways_dikeside: KoswatSurroundingsProtocol

    waters_polderside: KoswatWatersPolderside
    waters_dikeside: KoswatSurroundingsProtocol

    roads_class_2_polderside: KoswatSurroundingsProtocol
    roads_class_7_polderside: KoswatSurroundingsProtocol
    roads_class_24_polderside: KoswatSurroundingsProtocol
    roads_class_47_polderside: KoswatSurroundingsProtocol
    roads_class_unknown_polderside: KoswatSurroundingsProtocol

    roads_class_2_dikeside: KoswatSurroundingsProtocol
    roads_class_7_dikeside: KoswatSurroundingsProtocol
    roads_class_24_dikeside: KoswatSurroundingsProtocol
    roads_class_47_dikeside: KoswatSurroundingsProtocol
    roads_class_unknown_dikeside: KoswatSurroundingsProtocol

    def __init__(self) -> None:
        self.dike_section = ""
        self.traject = ""
        self.subtraject = ""

        self.buildings_polderside = None
        self.buildings_dikeside = None
        self.railways_polderside = None
        self.railways_dikeside = None
        self.waters_polderside = None
        self.waters_dikeside = None
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

    @property
    def locations(self) -> list[PointSurroundings]:
        """
        Each location represents 1 meter in a real scale map.

        Returns:
            List[PointSurroundings]: List of points along the polderside.
        """
        if not self.buildings_polderside:
            return []
        return self.buildings_polderside.points

    def get_locations_after_distance(self, distance: float) -> list[Point]:
        """
        Gets all locations which are safe from surroundings (building/railway/water) in a radius of `distance`.

        Args:
            distance (float): Radius from each point that should be free of buildings.

        Returns:
            List[Point]: List of safe locations (points).
        """

        def is_at_safe_distance(point_surroundings: PointSurroundings) -> bool:
            if not point_surroundings.distance_to_surroundings:
                return True
            return distance < point_surroundings.distance_to_surroundings[0]

        if not self.buildings_polderside:
            return []

        return list(filter(is_at_safe_distance, self.buildings_polderside.points))
