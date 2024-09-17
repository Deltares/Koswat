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
            infrastructure_width=2.4,
            points=[
                PointSurroundings(
                    location=Point(2.4, 4.2), surroundings_matrix={5: 1.5, 10: 3, 15: 6}
                )
            ],
        )

    def test_given_infrastructure_fixture_calculates_costs(
        self, surroundings_infrastructure_fixture: SurroundingsInfrastructure
    ):
        # 1. Define test data.
        _surtax_costs = 1.0
        _zone_a_costs = 2.0
        _zone_b_costs = 3.0
        _calculator = InfrastructureProfileCostsCalculator(
            infrastructure=surroundings_infrastructure_fixture,
            surtax_costs=_surtax_costs,
            zone_a_costs=_zone_a_costs,
            zone_b_costs=_zone_b_costs,
        )

        # 2. Run test.
        _locations_costs = _calculator.calculate(4.2, 42)

        # 3. Verify expectations.
        assert isinstance(_locations_costs, list)
        assert len(_locations_costs) == 1
        assert isinstance(_locations_costs[0], InfrastructureLocationCosts)
        _location_cost = _locations_costs[0]
        assert (
            _location_cost.location
            == surroundings_infrastructure_fixture.points[0].location
        )
        assert _location_cost.surtax_costs == _surtax_costs
        assert _location_cost.zone_a_costs == _zone_a_costs
        assert _location_cost.zone_b_costs == _zone_b_costs
        assert _location_cost.zone_a == math.nan
        assert _location_cost.zone_b == math.nan
