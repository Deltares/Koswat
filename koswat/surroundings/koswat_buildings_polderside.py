from typing import List

from shapely.geometry import Point

from koswat.surroundings.surroundings_protocol import SurroundingsProtocol


class PointSurroundings:
    section: str = ""
    location: Point = None
    distance_to_buildings: List[float] = []


class KoswatBuildingsPolderside(SurroundingsProtocol):
    points: List[PointSurroundings] = []

    @property
    def conflicting_points(self) -> List[PointSurroundings]:
        return [_cf for _cf in self.points if any(_cf.distance_to_buildings)]
