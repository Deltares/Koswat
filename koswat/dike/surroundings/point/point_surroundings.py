import math
from dataclasses import dataclass, field

from shapely.geometry import Point


@dataclass
class PointSurroundings:
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

    @property
    def closest_obstacle(self) -> float:
        """
        Distance to the closest (obstacle) surrounding. When no surroundings are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for buildings at distance 0.

        Returns:
            float: Distance to the closest surrounding.
        """

        return min(
            (
                _s_key
                for _s_key, _s_value in self.surroundings_matrix.items()
                # Ensure we do return a key which actually has a surrounding.
                if _s_value > 0
            ),
            default=math.nan,
        )

    def get_total_infrastructure_width(
        self, from_limit: float, to_limit: float
    ) -> float:
        """
        Calculates what is the total width of infrastructures found between two distances
        `from_limit` and `to_limit`.

        Args:
            from_limit (float): Lower limit from where we can start looking for infrastructures.
            to_limit (float): Upper limit from where we can finish looking for infrastructures.

        Returns:
            float: The total length of infrastructures found between two points.
        """

        _total_width = 0
        for k, v in sorted(self.surroundings_matrix.items(), key=lambda item: item[0]):
            if k > from_limit or math.isclose(k, from_limit):
                _total_width += v
                if k > to_limit or math.isclose(k, to_limit):
                    break

        return _total_width
