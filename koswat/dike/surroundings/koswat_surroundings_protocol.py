from typing import Protocol, runtime_checkable

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@runtime_checkable
class KoswatSurroundingsProtocol(Protocol):
    """
    Empty interface to represent the Koswat surroundings and easily identify them throughout the solution.
    """

    points: list[PointSurroundings]
