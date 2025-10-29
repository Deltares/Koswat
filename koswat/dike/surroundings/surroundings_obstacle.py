from dataclasses import dataclass, field

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_obstacle_surroundings import PointObstacleSurroundings


@dataclass
class SurroundingsObstacle(KoswatSurroundingsProtocol):
    """
    Defines surroundings point collections that cannot be repaired or replaced.
    The `PointObstacleSurroundings` contain the closest distance to an obstacle
    both inside and outside the polder.
    """

    points: list[PointObstacleSurroundings] = field(default_factory=lambda: [])
