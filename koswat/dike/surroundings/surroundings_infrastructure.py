import math
from dataclasses import dataclass, field

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class SurroundingsInfrastructure(KoswatSurroundingsProtocol):
    """
    Defines surroundings point collections that can be repaired or replaced.

    The `PointSurroundings` contain a matrix (dictionary) where the keys
    represent the distances to an obstacle, and the values a float representing
    how long that infrastructure is.
    """

    points: list[PointSurroundings] = field(default_factory=lambda: [])
    infrastructure_width: float = math.nan
