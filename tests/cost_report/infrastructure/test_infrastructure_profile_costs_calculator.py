import math
from typing import Callable, Iterable

import pytest
from shapely import Point

from koswat.cost_report.infrastructure.infrastructure_location_costs import (
    InfrastructureLocationCosts,
)
from koswat.cost_report.infrastructure.infrastructure_profile_costs_calculator import (
    InfrastructureProfileCostsCalculator,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from tests.conftest import PointSurroundingsTestCase


class TestInfrastructureProfileCostsCalculator:
    def test_initialize(self):
        # 1. Define test data.
        _calculator = InfrastructureProfileCostsCalculator()

        # 2. Verify expectations.
        assert isinstance(_calculator, InfrastructureProfileCostsCalculator)
        assert not _calculator.infrastructure
        assert math.isnan(_calculator.surtax_costs)
        assert math.isnan(_calculator.zone_a_costs)
        assert math.isnan(_calculator.zone_b_costs)

    @pytest.fixture(name="surroundings_infrastructure_fixture")
    def _get_surroundings_infrastructure_fixture(
        self,
        point_surroundings_for_zones_builder_fixture: tuple[
            Callable[[], PointSurroundings], PointSurroundingsTestCase
        ],
    ) -> Iterable[SurroundingsInfrastructure]:
        _builder, test_case = point_surroundings_for_zones_builder_fixture
        yield SurroundingsInfrastructure(
            infrastructure_name="dummy infrastructure",
            # To simplify A / B total areas, we just set it to `1`.
            infrastructure_width=1,
            points=[_builder()],
        ), test_case

    def test_given_infrastructure_fixture_calculates_costs(
        self,
        surroundings_infrastructure_fixture: tuple[
            SurroundingsInfrastructure, PointSurroundingsTestCase
        ],
    ):
        """
        This test validates that the matrix costs (e.g.: {0: a, 5: b, 10: c})
        will be used so that based on the width of the `zone_a` we round up its value
        until a key match is found.
        For instance if `zone_a = 4` then the costs will be
        the addition of all values between `0` and `5`, both included,
        therefore `zone_a_costs = a + b`.
        For `zone_b` we ignore those keys already taken
        by `zone_a`. So if `zone_b = 1` then we look for the range `[zone_a, zone_a+zone_b]`
        which translates to `[4, 5]`, thus taking keys `0`, `5`, and `10`. Because the
        first two were claimed by `zone_a` we simply calculate `zone_b_costs = c`.

        TODO: What happens when the strategy costs for zone a are either `GEEN` or `HERSTEL`?
        """
        # 1. Define test data.
        # Set costs to 1 for easy comparisons.
        _surtax_costs = 1.0
        _zone_a_costs = 1.0
        _zone_b_costs = 1.0
        (
            _infrastructure_fixture,
            _point_surroundings_case,
        ) = surroundings_infrastructure_fixture
        _calculator = InfrastructureProfileCostsCalculator(
            infrastructure=_infrastructure_fixture,
            surtax_costs=_surtax_costs,
            zone_a_costs=_zone_a_costs,
            zone_b_costs=_zone_b_costs,
        )

        # 2. Run test.
        _locations_costs = _calculator.calculate(
            _point_surroundings_case.zone_a_width, _point_surroundings_case.zone_b_width
        )

        # 3. Verify expectations.
        assert isinstance(_locations_costs, list)
        assert len(_locations_costs) == 1
        assert isinstance(_locations_costs[0], InfrastructureLocationCosts)
        _location_cost = _locations_costs[0]
        assert (
            _location_cost.location.location
            == _infrastructure_fixture.points[0].location
        )
        assert _location_cost.surtax_costs == _surtax_costs
        assert (
            _location_cost.zone_a_costs
            == _zone_a_costs * _point_surroundings_case.expected_total_widths[0]
        )
        assert (
            _location_cost.zone_b_costs
            == _zone_b_costs * _point_surroundings_case.expected_total_widths[1]
        )
        assert (
            _location_cost.zone_a == _point_surroundings_case.expected_total_widths[0]
        )
        assert (
            _location_cost.zone_b == _point_surroundings_case.expected_total_widths[1]
        )
