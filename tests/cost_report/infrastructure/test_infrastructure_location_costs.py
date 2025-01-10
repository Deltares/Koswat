from koswat.cost_report.infrastructure.infrastructure_location_costs import (
    InfrastructureLocationCosts,
)


class TestInfrastructureLocationCosts:
    def test_initialization(self):
        # 1. Initialize class
        _infra_location_costs = InfrastructureLocationCosts()

        # 2. Verify expectations.
        assert isinstance(_infra_location_costs, InfrastructureLocationCosts)
        assert not _infra_location_costs.location

        # Verify default values are not `math.nan``.
        # (Otherwise the `.csv` files could become invalid)
        assert _infra_location_costs.zone_a == 0
        assert _infra_location_costs.zone_b == 0
        assert _infra_location_costs.zone_a_costs == 0
        assert _infra_location_costs.zone_b_costs == 0
        assert _infra_location_costs.surtax == 0
        assert _infra_location_costs.total_cost == 0
