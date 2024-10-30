from cgitb import small
from typing import Iterator

import pytest
from mergedeep import Strategy

from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.vps_reinforcement_profile import (
    VPSReinforcementProfile,
)
from koswat.strategies.infra_priority_strategy.infra_cluster import InfraCluster
from koswat.strategies.infra_priority_strategy.infra_priority_strategy import (
    InfraPriorityStrategy,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_protocol import StrategyProtocol
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)
from tests.dike.surroundings import point


class TestInfraPriorityStrategy:
    def test_initialize(self):
        # 1. Define and run test data.
        _strategy = InfraPriorityStrategy()

        # 2. Verify expectations.
        assert isinstance(_strategy, InfraPriorityStrategy)
        assert isinstance(_strategy, StrategyProtocol)

    def test_given_example_when_apply_strategy_then_gets_new_ones(
        self, example_strategy_input: StrategyInput
    ):
        # 1. Define test data.
        assert isinstance(example_strategy_input, StrategyInput)

        # 2. Run test.
        _strategy_result = InfraPriorityStrategy().apply_strategy(
            example_strategy_input
        )

        # 3. Verify final expectations.
        assert isinstance(_strategy_result, list)
        assert len(_strategy_result) == len(example_strategy_input.strategy_locations)
        assert all(
            isinstance(_sr, StrategyLocationReinforcement) for _sr in _strategy_result
        )

        # Basically the same checks as in `test__apply_min_distance_given_example`.
        assert all(
            _sr.selected_measure == PipingWallReinforcementProfile
            for _sr in _strategy_result[0:2]
        )
        assert all(
            _sr.selected_measure == CofferdamReinforcementProfile
            for _sr in _strategy_result[2:]
        )

    def test_given_example_for_subclusters_when_apply_strategy_then_splits_them(
        self, example_subclustering: StrategyInput
    ):
        # 1. Define test data.
        assert isinstance(example_subclustering, StrategyInput)

        # 2. Run test.
        _strategy_result = InfraPriorityStrategy().apply_strategy(example_subclustering)

        # 3. Verify final expectations.
        assert isinstance(_strategy_result, list)
        assert len(_strategy_result) == len(example_subclustering.strategy_locations)
        assert all(
            isinstance(_sr, StrategyLocationReinforcement) for _sr in _strategy_result
        )

        # Basically the same checks as in `test__apply_min_distance_given_example`.
        assert all(
            _sr.selected_measure == PipingWallReinforcementProfile
            for _sr in _strategy_result[0:2]
        )
        assert all(
            _sr.selected_measure == StabilityWallReinforcementProfile
            for _sr in _strategy_result[2:5]
        )
        assert all(
            _sr.selected_measure == CofferdamReinforcementProfile
            for _sr in _strategy_result[5:]
        )

    @pytest.fixture(name="small_infra_cluster")
    def _get_small_infra_cluster_fixture(self) -> Iterator[InfraCluster]:
        yield InfraCluster(
            reinforcement_type=SoilReinforcementProfile,
            min_required_length=2,
            cluster=[],
        )

    @pytest.mark.parametrize(
        "subcluster_min_length_addition",
        [
            pytest.param(0, id="Same size as Infra cluster"),
            pytest.param(1, id="Bigger than size of Infra cluster"),
        ],
    )
    def test_given_small_cluster_when_generate_subcluster_options_then_returns_it_back(
        self, small_infra_cluster: InfraCluster, subcluster_min_length_addition: int
    ):
        # 1. Define test data.
        assert isinstance(small_infra_cluster, InfraCluster)
        _subcluster_min_length = (
            len(small_infra_cluster.cluster) + subcluster_min_length_addition
        )

        # 2. Run test.
        _return_value = InfraPriorityStrategy.generate_subcluster_options(
            small_infra_cluster, _subcluster_min_length
        )

        # 3. Verify expectations.
        assert isinstance(_return_value, list)
        assert len(_return_value) == 1
        assert isinstance(_return_value[0], list)
        assert len(_return_value[0]) == 1
        assert _return_value[0][0] == small_infra_cluster

    @pytest.fixture(name="infra_cluster_for_subclusters")
    def _get_infra_cluster_for_subclusters_fixture(self) -> Iterator[InfraCluster]:

        _common_reinforcements = [
            SoilReinforcementProfile,
            VPSReinforcementProfile,
            PipingWallReinforcementProfile,
        ]
        _available_measures_per_location = [
            _common_reinforcements + [CofferdamReinforcementProfile],
            _common_reinforcements,
            _common_reinforcements,
            _common_reinforcements + [StabilityWallReinforcementProfile],
        ]
        _location_input = StrategyLocationInput(
            point_surrounding=None,
            strategy_reinforcement_type_costs=[
                StrategyReinforcementTypeCosts(
                    SoilReinforcementProfile, base_costs=42, infrastructure_costs=420000
                ),
                StrategyReinforcementTypeCosts(
                    PipingWallReinforcementProfile,
                    base_costs=4200,
                    infrastructure_costs=420,
                ),
                # Costs are too big, it won't be considered
                StrategyReinforcementTypeCosts(
                    VPSReinforcementProfile,
                    base_costs=42000000,
                    infrastructure_costs=4200000,
                ),
                # Not present at all locations.
                StrategyReinforcementTypeCosts(
                    StabilityWallReinforcementProfile,
                    base_costs=42,
                    infrastructure_costs=42,
                ),
                # Cheapest of all, but only present at one location.
                StrategyReinforcementTypeCosts(
                    CofferdamReinforcementProfile, base_costs=42, infrastructure_costs=0
                ),
            ],
        )

        _cluster_data = []
        for _available_measures in _available_measures_per_location:
            _slr = StrategyLocationReinforcement(
                location=None,
                available_measures=_available_measures,
                strategy_location_input=_location_input,
            )
            _slr.selected_measure = SoilReinforcementProfile
            _cluster_data.append(_slr)

        yield InfraCluster(
            reinforcement_type=SoilReinforcementProfile,
            min_required_length=2,
            cluster=_cluster_data,
        )

    def test_given_cluster_when_generate_sbucluster_options_returns(
        self, infra_cluster_for_subclusters: InfraCluster
    ):
        # 1. Define test data.
        assert isinstance(infra_cluster_for_subclusters, InfraCluster)
        _min_cluster_len = int(len(infra_cluster_for_subclusters.cluster) / 2)

        # 2. Run test.
        _options = list(
            InfraPriorityStrategy.generate_subcluster_options(
                infra_cluster_for_subclusters, _min_cluster_len
            )
        )

        # 3. Verify expectations.
        assert len(_options) == 2
        for _option in _options:
            assert len(_option) == 2
            for _subcluster in _option:
                assert isinstance(_subcluster, InfraCluster)
                assert all(
                    _sc in infra_cluster_for_subclusters.cluster
                    for _sc in _subcluster.cluster
                )

    def test_given_cluster_when_get_common_available_measures_costs_then_returns_dict(
        self, infra_cluster_for_subclusters: InfraCluster
    ):
        # 1. Define test data.
        _expected_common_reinforcements = [
            SoilReinforcementProfile,
            PipingWallReinforcementProfile,
        ]
        assert infra_cluster_for_subclusters.is_valid()

        # 2. Run test.
        _costs_dict = InfraPriorityStrategy.get_common_available_measures_costs(
            infra_cluster_for_subclusters,
            OrderStrategy.get_default_order_for_reinforcements(),
        )

        # 3. Verify expectations.
        assert isinstance(_costs_dict, dict)
        assert len(_costs_dict.keys()) == len(_expected_common_reinforcements)

        # Only the common types are in the costs dictionary.
        def validate_costs_for_profile(
            reinforcement_type: type[ReinforcementProfileProtocol],
        ):
            assert reinforcement_type in _costs_dict
            _sr_costs = infra_cluster_for_subclusters.cluster[
                0
            ].get_reinforcement_costs(reinforcement_type)
            assert _costs_dict[reinforcement_type] == pytest.approx(
                _sr_costs * len(infra_cluster_for_subclusters.cluster)
            )

        for _expected_type in _expected_common_reinforcements:
            validate_costs_for_profile(_expected_type)
