from typing import Iterator

import pytest

from koswat.dike_reinforcements.reinforcement_profile.standard.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.strategies.infra_priority_strategy.infra_cluster import InfraCluster
from koswat.strategies.infra_priority_strategy.infra_cluster_option import (
    InfraClusterOption,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class TestInfraClusterOption:
    def test_initialize(self):
        # 1. Define test data
        _min_length = 2

        # 2. Run test.
        _option = InfraClusterOption(_min_length)

        # 3. Verify expectations.
        assert isinstance(_option, InfraClusterOption)
        assert not _option.cluster_collection
        assert not _option.cluster_costs
        assert not _option.valid_option()

    @pytest.fixture(name="dummy_option")
    def _get_dummy_option_fixture_for_simple_tests(
        self,
    ) -> Iterator[InfraClusterOption]:
        yield InfraClusterOption(cluster_min_length=2)

    def test_given_invalid_cluster_in_option_when_valid_option_then_is_false(
        self, dummy_option: InfraClusterOption
    ):
        # 1. Define test data.
        assert not dummy_option.valid_option()

        _simple_cluster = InfraCluster(
            reinforcement_type=None, min_required_length=4, cluster=[]
        )
        assert not _simple_cluster.is_valid()

        # 2. Run test
        dummy_option.add_cluster(_simple_cluster, {})

        # 3. Verify expectations
        assert not dummy_option.valid_option()

    def test_given_valid_cluster_in_option_when_valid_option_then_is_true(
        self, dummy_option: InfraClusterOption
    ):
        # 1. Define test data.
        assert not dummy_option.valid_option()

        _simple_cluster = InfraCluster(
            reinforcement_type=None,
            min_required_length=10 * dummy_option._cluster_min_length,
            cluster=[0] * dummy_option._cluster_min_length,
        )
        # Ironically, the current logic allows for this to be valid
        assert not _simple_cluster.is_valid()

        # 2. Run test
        dummy_option.add_cluster(_simple_cluster, {})

        # 3. Verify expectations.
        assert dummy_option.valid_option()

    @pytest.fixture(name="valid_option")
    def _get_valid_option_fixture(self) -> Iterator[InfraClusterOption]:
        _option = InfraClusterOption(cluster_min_length=1)
        _option.add_cluster(
            InfraCluster(
                reinforcement_type=SoilReinforcementProfile,
                min_required_length=0,
                cluster=[
                    StrategyLocationReinforcement(
                        location=None,
                        selected_measure=SoilReinforcementProfile,
                        available_measures=[],
                    )
                ],
            ),
            {SoilReinforcementProfile: 42000, PipingWallReinforcementProfile: 42},
        )
        yield _option

    def test_given_valid_cluster_when_set_cheapest_option_then_updates_clusters(
        self, valid_option: InfraClusterOption
    ):
        # 1. Define test data.
        _current_selection = SoilReinforcementProfile
        _new_selection = PipingWallReinforcementProfile
        assert valid_option.valid_option()
        assert all(
            _oc.reinforcement_type == _current_selection
            for _oc in valid_option.cluster_collection
        )

        # 2. Run test.
        valid_option.set_cheapest_option()

        # 3. Verify expectations.
        assert all(
            _oc.reinforcement_type == _new_selection
            for _oc in valid_option.cluster_collection
        )
