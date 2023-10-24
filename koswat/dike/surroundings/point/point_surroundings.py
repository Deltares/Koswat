import math

from shapely.geometry import Point


class PointSurroundings:
    """
    Object representing a `meter` with `x`, `y` coordinates in a polder (or else).
    """

    section: str
    traject_order: int
    location: Point
    distance_to_surroundings: list[float]

    def __init__(self) -> None:
        self.section = ""
        self.location = None
        self.traject_order = -1
        self.distance_to_surroundings = []

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

    @property
    def closest_surrounding(self) -> float:
        """
        Distance to the closest surrounding (building/railway/water). When no surroundings are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for buildings at distance 0.

        Returns:
            float: Distance to the closest surrounding.
        """
        return min(self.distance_to_surroundings, default=math.nan)
