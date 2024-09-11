import math
from collections import defaultdict

from shapely.geometry import Point

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class KoswatSurroundingsPolderside(KoswatSurroundingsProtocol):
    points: list[PointSurroundings]

    def __init__(self) -> None:
        self.points = []

    @property
    def conflicting_points(self) -> list[PointSurroundings]:
        return [_cf for _cf in self.points if any(_cf.distance_to_surroundings)]
