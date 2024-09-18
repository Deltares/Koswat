import math
from typing import Iterable

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
    ) -> Iterable[SurroundingsInfrastructure]:
        yield SurroundingsInfrastructure(
            infrastructure_name="dummy infrastructure",
            # To simplify A / B total areas, we just set it to `1`.
            infrastructure_width=1,
            points=[
                PointSurroundings(
                    location=Point(2.4, 4.2), surroundings_matrix={5: 1.5, 10: 3, 15: 6}
                )
            ],
        )

    @pytest.mark.parametrize(
        "zone_a_width, zone_b_width, expected_total_widths",
        [
            pytest.param(4, 4, (1.5, 3), id="'A' [0, 4], 'B' [4, 8]"),
            pytest.param(5, 4, (1.5, 3), id="'A' [0, 5], 'B' [5, 9]"),
            pytest.param(4, 10, (1.5, 9), id="'A' [0, 4], 'B' [4, 14]"),
            pytest.param(5, 10, (1.5, 9), id="'A' [0, 5], 'B' [5, 15]"),
            pytest.param(0, 8, (0, 4.5), id="'B' [0, 8]"),
            pytest.param(0, 10, (0, 4.5), id="'B' [0, 10]"),
            pytest.param(0, 12, (0, 10.5), id="'B' [0, 12]"),
        ],
    )
    def test_given_infrastructure_fixture_calculates_costs(
        self,
        zone_a_width: float,
        zone_b_width: float,
        expected_total_widths: tuple[float, float],
        surroundings_infrastructure_fixture: SurroundingsInfrastructure,
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
        _calculator = InfrastructureProfileCostsCalculator(
            infrastructure=surroundings_infrastructure_fixture,
            surtax_costs=_surtax_costs,
            zone_a_costs=_zone_a_costs,
            zone_b_costs=_zone_b_costs,
        )

        # 2. Run test.
        _locations_costs = _calculator.calculate(zone_a_width, zone_b_width)

        # 3. Verify expectations.
        assert isinstance(_locations_costs, list)
        assert len(_locations_costs) == 1
        assert isinstance(_locations_costs[0], InfrastructureLocationCosts)
        _location_cost = _locations_costs[0]
        assert (
            _location_cost.location.location
            == surroundings_infrastructure_fixture.points[0].location
        )
        assert _location_cost.surtax_costs == _surtax_costs
        assert _location_cost.zone_a_costs == _zone_a_costs * expected_total_widths[0]
        assert _location_cost.zone_b_costs == _zone_b_costs * expected_total_widths[1]
        assert _location_cost.zone_a == expected_total_widths[0]
        assert _location_cost.zone_b == expected_total_widths[1]
