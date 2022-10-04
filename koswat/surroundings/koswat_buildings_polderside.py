from typing import List

from shapely.geometry import Point

from koswat.surroundings.surroundings_protocol import SurroundingsProtocol


class PointSurroundings:
    section: str = ""
    location: Point = None
    distance_to_buildings: List[float] = []


class KoswatBuildingsPolderside(SurroundingsProtocol):
    conflicting_points: List[PointSurroundings] = []
