from dataclasses import dataclass, field

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class SurroundingsInfrastructure(KoswatSurroundingsProtocol):
    """
    Defines surroundings point collections that can be removed or reworked.
    """

    points: list[PointSurroundings] = field(default_factory=lambda: [])

