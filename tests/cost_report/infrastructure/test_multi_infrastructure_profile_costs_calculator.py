from typing import Callable, Iterable

import pytest

from koswat.cost_report.infrastructure.infrastructure_location_profile_cost_report import (
    InfrastructureLocationProfileCostReport,
)
from koswat.cost_report.infrastructure.infrastructure_profile_costs_calculator import (
    InfrastructureProfileCostsCalculator,
)
from koswat.cost_report.infrastructure.multi_infrastructure_profile_costs_calculator import (
    MultiInfrastructureProfileCostsCalculator,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class TestMultiInfrastructureProfileCostsCalculator:
    def test_initialize(self):
        # 1. Define data.
        _calculator = MultiInfrastructureProfileCostsCalculator()

        # 2. Verify expectations.
        assert isinstance(_calculator, MultiInfrastructureProfileCostsCalculator)
        assert not _calculator.infrastructure_calculators

    @pytest.fixture(name="infra_profile_cost_calc_builder")
    def _get_infrastructure_profile_cost_calculator_builder_fixture(
        self,
        basic_point_surroundings_builder: Callable[[], PointSurroundings],
    ) -> Iterable[Callable[[int], InfrastructureProfileCostsCalculator]]:
        def build_calculator(n_points: int) -> InfrastructureProfileCostsCalculator:
            _infra = SurroundingsInfrastructure(
                infrastructure_name="dummy infrastructure",
                # To simplify A / B total areas, we just set it to `1`.
                infrastructure_width=1,
                points=[basic_point_surroundings_builder()] * n_points,
            )
            return InfrastructureProfileCostsCalculator(
                infrastructure=_infra,
                surtax=1.0,
                zone_a_costs=1.0,
                zone_b_costs=1.0,
            )

        yield build_calculator

    def test_given_reinforced_profile_generates_report_per_infrastructure_location(
        self,
        reinforcement_profile_builder: Callable[
            [list[tuple[float]], list[tuple[float]]], ReinforcementProfileProtocol
        ],
        infra_profile_cost_calc_builder: Callable[
            [int], InfrastructureProfileCostsCalculator
        ],
    ):
        # 1. Define data.
        _calc_with_two_locations = infra_profile_cost_calc_builder(2)
        _calc_with_one_location = infra_profile_cost_calc_builder(1)
        _waterside_reinforced_points = [(-18, 0), (-18, 0), (-18, 0)]
        _points_base_profile = _waterside_reinforced_points + [
            (0, 6),
            (10, 6),
            (34, -2),
            (34, -2),
            (34, -2),
        ]

        _points_reinforced_profile = _waterside_reinforced_points + [
            (0, 6),
            (10, 6),
            (34, -2),
            (34, -2),
            (34, -2),
        ]

        # 2. Run test
        _reports = MultiInfrastructureProfileCostsCalculator(
            infrastructure_calculators=[
                _calc_with_one_location,
                _calc_with_two_locations,
            ]
        ).calculate(
            reinforcement_profile_builder(
                _points_base_profile, _points_reinforced_profile
            )
        )

        # 3. Verify epxectations
        assert isinstance(_reports, list)
        assert len(_reports) == 3
        # assert all(
        #     isinstance(_r, InfrastructureLocationProfileCostReport) for _r in _reports
        # )
