import math
from typing import Iterator

import pytest

from koswat.dike_reinforcements.reinforcement_profile.standard.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.strategies.infra_priority_strategy.infra_cluster import InfraCluster
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class TestInfraCluster:
    def test_initialize(self):
        # 1. Define test data.
        _reinforcement_type = None
        _min_length = 42

        # 2. Run test.
        _infra_cluster = InfraCluster(
            reinforcement_type=_reinforcement_type, min_required_length=_min_length
        )

        # 3. Verify expectations
        assert isinstance(_infra_cluster, InfraCluster)
        assert _infra_cluster.reinforcement_type == _reinforcement_type
        assert _infra_cluster.min_required_length == _min_length
        assert not any(_infra_cluster.cluster)
        assert not _infra_cluster.is_valid()
        assert not _infra_cluster.fits_subclusters()
        assert math.isnan(_infra_cluster.current_cost)

    @pytest.fixture(name="cluster_fixture")
    def _get_basic_cluster_fixture(self) -> Iterator[InfraCluster]:
        yield InfraCluster(
            reinforcement_type=SoilReinforcementProfile, min_required_length=2
        )

    def test_given_cluster_min_length_when_is_valid_returns_true(
        self, cluster_fixture: InfraCluster
    ):
        # 1. Define test data.
        assert not cluster_fixture.is_valid()
        assert cluster_fixture.min_required_length > 0
        cluster_fixture.cluster = [0] * cluster_fixture.min_required_length

        # 2. Run test.
        assert cluster_fixture.is_valid()

    @pytest.mark.parametrize(
        "cluster_length",
        [
            pytest.param(2, id="Same size as fixture min required"),
            pytest.param(3, id="Bigger than fixture min required"),
        ],
    )
    def test_given_cluster_length_when_fits_subcluster_returns_false(
        self, cluster_fixture: InfraCluster, cluster_length: int
    ):
        # 1. Define test data.
        assert cluster_fixture.min_required_length <= cluster_length
        cluster_fixture.cluster = [0] * cluster_length
        assert cluster_fixture.is_valid()

        # 2. Run test.
        assert not cluster_fixture.fits_subclusters()

    def test_given_cluster_twice_min_length_when_fits_subcluster_returns_true(
        self, cluster_fixture: InfraCluster
    ):
        # 1. Define test data.
        assert cluster_fixture.min_required_length > 0
        cluster_fixture.cluster = [0] * cluster_fixture.min_required_length

        assert cluster_fixture.is_valid()
        assert not cluster_fixture.fits_subclusters()
        cluster_fixture.cluster = [0] * (2 * cluster_fixture.min_required_length)

        # 2. Run test.
        assert cluster_fixture.fits_subclusters()

    def test_set_cheapest_common_available_measure(self, cluster_fixture: InfraCluster):
        # 1. Define test data.
        _costs_dict = {
            SoilReinforcementProfile: 4200,
            PipingWallReinforcementProfile: 42,
        }
        assert cluster_fixture.reinforcement_type == SoilReinforcementProfile
        _slr = StrategyLocationReinforcement(
            location=None,
            available_measures=[cluster_fixture.reinforcement_type],
        )
        cluster_fixture.cluster = [_slr] * cluster_fixture.min_required_length
        assert cluster_fixture.is_valid()

        # 2. Run test.
        cluster_fixture.set_cheapest_common_available_measure(_costs_dict)

        # 3. Verify expectations.
        assert all(
            c.current_selected_measure == PipingWallReinforcementProfile
            for c in cluster_fixture.cluster
        )
