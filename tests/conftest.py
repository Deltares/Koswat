from dataclasses import dataclass
from typing import Callable, Iterable

import pytest
from shapely import Point

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings

_point_surroundings_cases = [
    pytest.param(4, 4, (1.5, 3), id="'A' [0, 4], 'B' [4, 8]"),
    pytest.param(5, 4, (1.5, 3), id="'A' [0, 5], 'B' [5, 9]"),
    pytest.param(4, 10, (1.5, 9), id="'A' [0, 4], 'B' [4, 14]"),
    pytest.param(5, 10, (1.5, 9), id="'A' [0, 5], 'B' [5, 15]"),
    pytest.param(0, 8, (0, 4.5), id="'B' [0, 8]"),
    pytest.param(0, 10, (0, 4.5), id="'B' [0, 10]"),
    pytest.param(0, 12, (0, 10.5), id="'B' [0, 12]"),
]


@dataclass
class PointSurroundingsTestCase:
    zone_a_width: float
    zone_b_width: float
    expected_total_widths: list[float, float]

    @property
    def zone_a_limits(self) -> tuple[float, float]:
        return (0, self.zone_a_width)

    @property
    def zone_b_limits(self) -> tuple[float, float]:
        return (self.zone_a_width, self.zone_b_width + self.zone_a_width)


@pytest.fixture(
    name="point_surroundings_for_zones_builder_fixture",
    params=[_psc.values for _psc in _point_surroundings_cases],
    ids=[_psc.id for _psc in _point_surroundings_cases],
)
def _get_point_surroundings_for_zones_builder_fixture(
    request: pytest.FixtureRequest,
) -> Iterable[tuple[Callable[[], PointSurroundings], PointSurroundingsTestCase]]:
    def build_point_surroundings() -> PointSurroundings:
        return PointSurroundings(
            location=Point(2.4, 4.2), surroundings_matrix={5: 1.5, 10: 3, 15: 6}
        )

    yield build_point_surroundings, PointSurroundingsTestCase(
        zone_a_width=request.param[0],
        zone_b_width=request.param[1],
        expected_total_widths=list(request.param[2]),
    )
