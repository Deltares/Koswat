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

    def get_total_infrastructure_per_zone(
        self, *zone_limit_collection: tuple[float, float]
    ) -> list[float]:
        """
        Gets the total infrastructure width at each of the provided zones
        `zone_limit_collection` (`tuple[float, float]`).
        The zone limits are matched by rounding up their upper limit to the
        `surroundings_matrix` keys (distances to the `location` in the real world).
        When two zones have overlapping limits (as expected) the lower one will
        "claim" the corresponding surrounding distance.

        Example:
            - `zone_limit_collection` = (0, 4), (4, 11)
            - `surroundings_matrix` = {5: 1.5, 10: 3, 15: 6}
            - "Taken" distances per zone:
                - `(0, 4)` takes key `5`.
                - `(4, 11)` takes key(s) `10` and `15` because `5` was already taken.
            - Total infrastructure width at zones = `(1.5, 9)`

        Returns:
            list[float]: list with total width corresponding to each provided zone.
        """

        # Prepare data.
        _sorted_matrix_array = sorted(
            self.surroundings_matrix.items(), key=lambda item: item[0]
        )

        _taken_keys = []

        def matrix_idx_for_limits(limits: tuple[float, float]) -> float:
            _lower_limit, _upper_limit = limits
            if math.isclose(_upper_limit, 0, abs_tol=1e-09):
                return 0
            _total_width = 0
            for _matrix_distance, value in _sorted_matrix_array:
                if _matrix_distance in _taken_keys or (
                    _matrix_distance < _lower_limit
                    and not math.isclose(_matrix_distance, _lower_limit)
                ):
                    continue

                _total_width += value
                if value != 0:
                    _taken_keys.append(_matrix_distance)
                if _matrix_distance > _upper_limit or math.isclose(
                    _matrix_distance, _upper_limit
                ):
                    # We include the first value above the `upper_limit`,
                    # then we stop. (Design decission taken with PO).
                    break
            return _total_width

        return list(map(matrix_idx_for_limits, zone_limit_collection))


@dataclass
class PointObstacleSurroundings(PointSurroundings):
    """
    Object representing a `meter` with `x`, `y` coordinates in a polder (or else),
    extended with obstacle specific properties.
    """

    inside_distance: float = math.nan
    outside_distance: float = math.nan
    angle_inside: float = math.nan
    angle_outside: float = math.nan

    @property
    def closest_obstacle(self) -> float:
        """
        Distance to the closest (obstacle) surrounding. When no surroundings are given the value will be `NaN` (Not A Number), so that the value 0 is reserved for buildings at distance 0.

        Returns:
            float: Distance to the closest surrounding.
        """

        return self.inside_distance