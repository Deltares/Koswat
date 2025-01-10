from dataclasses import dataclass, field

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class SurroundingsObstacle(KoswatSurroundingsProtocol):
    """
    Defines surroundings point collections that cannot be repaired or replaced.
    The `PointSurroundings` contain a matrix (dictionary) where the keys
    represent the distances to an obstacle, and the values a `1` (obstacle present)
    or a `0` (obstacle not present).
    """

    points: list[PointSurroundings] = field(default_factory=lambda: [])
