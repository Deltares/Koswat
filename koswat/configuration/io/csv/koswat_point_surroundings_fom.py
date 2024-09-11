import math
from dataclasses import dataclass, field

from shapely.geometry import Point


@dataclass
class KoswatPointSurroundingsFom:
    """
    Object representing a `meter` with `x`, `y` coordinates in a polder (or else).
    """

    section: str = ""
    traject_order: int = -1
    location: Point | None = None
    surroundings_matrix: dict[float, float] = field(default_factory=dict)

    def __hash__(self) -> int:
        """
        Overriding of the "magic" hash operator required
        so that `PointSurroundings` can be used as a key in a python dict.
        """
        return hash(
            (
                self.section,
                self.traject_order,
                self.location,
            )
        )

    def __eq__(self, __value: object) -> bool:
        """
        Overriding of the "magic" equality operator required
        so that `PointSurroundings` can be used as a key in a python dict.
        """
        if not isinstance(__value, type(self)):
            return False
        return (self.location, self.section, self.traject_order) == (
            __value.location,
            __value.section,
            __value.traject_order,
        )
