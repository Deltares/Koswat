import math
from collections.abc import Callable, Iterable
from dataclasses import dataclass

import pytest
from shapely import Point

from koswat.dike.surroundings.point import (
    PointInfrastructureSurroundings,
    PointSurroundingsProtocol,
)

_point_surroundings_cases = [
    pytest.param(
        (4, 4, 4),
        0,
        ([-4, 0], [0, 4], [4, 8]),
        (2.0, 1.5, 3.0),
        id="'A' [-4, 0], 'B' [0, 4], 'C' [4, 8]",
    ),
    pytest.param(
        (4, 5, 4),
        0,
        ([-4, 0], [0, 5], [5, 9]),
        (2.0, 1.5, 3.0),
        id="'A' [-4, 0], 'B' [0, 5], 'C' [5, 9]",
    ),
    pytest.param(
        (4, 6, 3),
        0,
        ([-4, 0], [0, 6], [6, 9]),
        (2.0, 4.5, 0.0),
        id="'A' [-4, 0], 'B' [0, 6], 'C' [6, 9]",
    ),
    pytest.param(
        (9, 4, 4),
        0,
        ([-9, 0], [0, 4], [4, 8]),
        (6.0, 1.5, 3.0),
        id="'A' [-9, 0], 'B' [0, 4], 'C' [4, 8]",
    ),
    pytest.param(
        (4, 4, 10),
        0,
        ([-4, 0], [0, 4], [4, 14]),
        (2.0, 1.5, 9.0),
        id="'A' [-4, 0], 'B' [0, 4], 'C' [4, 14]",
    ),
    pytest.param(
        (4, 5, 10),
        0,
        ([-4, 0], [0, 5], [5, 15]),
        (2.0, 1.5, 9.0),
        id="'A' [-4, 0], 'B' [0, 5], 'C' [5, 15]",
    ),
    pytest.param(
        (4, 5, 10),
        3,
        ([-4, -3], [-3, 5], [5, 15]),
        (0.0, 3.5, 9.0),
        id="'A' [-4, -3], 'B' [-3, 5], 'C' [5, 15], buffer applied",
    ),
    pytest.param(
        (4, 0, 8),
        0,
        ([-4, 0], [math.nan, math.nan], [0, 8]),
        (2.0, 0.0, 4.5),
        id="'A' [-4, 0], 'C' [0, 8]",
    ),
    pytest.param(
        (4, 0, 10),
        0,
        ([-4, 0], [math.nan, math.nan], [0, 10]),
        (2.0, 0.0, 4.5),
        id="'A' [-4, 0], 'C' [0, 10]",
    ),
    pytest.param(
        (4, 0, 12),
        0,
        ([-4, 0], [math.nan, math.nan], [0, 12]),
        (2.0, 0.0, 10.5),
        id="'A' [-4, 0], 'C' [0, 12]",
    ),
    pytest.param(
        (9, 0, 12),
        0,
        ([-9, 0], [math.nan, math.nan], [0, 12]),
        (6.0, 0.0, 10.5),
        id="'A' [-9, 0], 'C' [0, 12]",
    ),
    pytest.param(
        (9, 0, 12),
        3,
        ([-9, -3], [math.nan, math.nan], [-3, 12]),
        (4.0, 0.0, 12.5),
        id="'A' [-9, -3], 'C' [-3, 12], buffer applied",
    ),
    pytest.param(
        (9, 0, 12),
        10,
        ([-9, -9], [math.nan, math.nan], [-9, 12]),
        (0.0, 0.0, 16.5),
        id="'A' [-9, -9], 'C' [-9, 12], buffer beyond width of A",
    ),
]


@dataclass
class PointSurroundingsTestCase:
    """
    Data class used to better handle the `pytest.FixtureRequest.param`
    when using fixture test cases (`params`).
    """

    zone_a_width: float
    zone_b_width: float
    zone_c_width: float
    zone_a_limits: tuple[float, float]
    zone_b_limits: tuple[float, float]
    zone_c_limits: tuple[float, float]
    crest_buffer: float
    expected_total_lengths: list[float]


@pytest.fixture(name="basic_point_surroundings_builder")
def _get_basic_point_surroundings_builder_fixture() -> (
    Iterable[Callable[[], PointSurroundingsProtocol]]
):
    def build() -> PointSurroundingsProtocol:
        return PointInfrastructureSurroundings(
            location=Point(2.4, 4.2),
            polderside_surroundings={5: 1.5, 10: 3.0, 15: 6.0},
            waterside_surroundings={5: 2.0, 10: 4.0, 15: 8.0},
        )

    yield build


@pytest.fixture(
    name="point_surroundings_for_zones_builder_fixture",
    params=[_psc.values for _psc in _point_surroundings_cases],
    ids=[_psc.id for _psc in _point_surroundings_cases],
)
def _get_point_surroundings_for_zones_builder_fixture(
    request: pytest.FixtureRequest,
    basic_point_surroundings_builder: Callable[[], PointSurroundingsProtocol],
) -> Iterable[
    tuple[Callable[[], PointSurroundingsProtocol], PointSurroundingsTestCase]
]:
    """
    Simple fixture that can be used as an example on how infrastructure widths are determined
    based on the reinforcement profile's zones `A`, `B` and `C`. Because we call directly and
    indirectly to the `PointInfrastructureSurroundings.get_total_infrastructure_per_zone` in different
    sub-projects we required having this fixture at the top-most test level.
    """

    yield basic_point_surroundings_builder, PointSurroundingsTestCase(
        zone_a_width=request.param[0][0],
        zone_b_width=request.param[0][1],
        zone_c_width=request.param[0][2],
        crest_buffer=request.param[1],
        zone_a_limits=request.param[2][0],
        zone_b_limits=request.param[2][1],
        zone_c_limits=request.param[2][2],
        expected_total_lengths=list(request.param[3]),
    )
