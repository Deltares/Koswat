from typing import Callable, Type

from shapely import Point

from koswat.cost_report.io.summary.summary_locations.cluster_shp_fom import (
    ClusterShpFom,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class TestClusterShapeFom:
    def test_points_with_neighbour_extent_without_neighbours(
        self,
        cluster_shp_fom_factory: Callable[
            [list[tuple[float, float]], Type[ReinforcementProfileProtocol], float],
            ClusterShpFom,
        ],
    ):
        # 1. Prepare test data.
        _first_xy = (10, 10)
        _last_xy = (20, 20)
        _cluster = cluster_shp_fom_factory(
            [_first_xy, _last_xy], SoilReinforcementProfile, 0.0
        )

        assert _cluster.left_neighbour_extent is None
        assert _cluster.right_neighbour_extent is None

        # 2. Run test.
        _points = _cluster.points_with_neighbour_extent

        # 3. Verify expectations.
        assert _points == [Point(_first_xy), Point(_last_xy)]

    def test_points_with_neighbour_extent_with_neighbours(
        self,
        cluster_shp_fom_factory: Callable[
            [list[tuple[float, float]], Type[ReinforcementProfileProtocol], float],
            ClusterShpFom,
        ],
    ):
        # 1. Prepare test data.
        _left_extent = Point(5, 5)
        _first_xy = (10, 10)
        _last_xy = (20, 20)
        _right_extent = Point(25, 25)

        _cluster = cluster_shp_fom_factory(
            [_first_xy, _last_xy], SoilReinforcementProfile, 0.0
        )

        # 2. Run test.
        _points = _cluster.points_with_neighbour_extent

        # 3. Verify expectations.
        assert _points == [
            _left_extent,
            Point(_first_xy),
            Point(_last_xy),
            _right_extent,
        ]

    def test_add_neighbour_extent(
        self,
        cluster_shp_fom_factory: Callable[
            [list[tuple[float, float]], Type[ReinforcementProfileProtocol], float],
            ClusterShpFom,
        ],
    ):
        # 1. Prepare test data.
        _left_last_xy = (20, 20)
        _right_first_xy = (30, 30)

        _expected_neighbour_extent = Point(25, 25)

        _left_cluster = cluster_shp_fom_factory(
            [(-99, -99), _left_last_xy], SoilReinforcementProfile, 0.0
        )
        _right_cluster = cluster_shp_fom_factory(
            [_right_first_xy, (99, 99)], SoilReinforcementProfile, 0.0
        )

        assert _left_cluster.right_neighbour_extent is None
        assert _right_cluster.left_neighbour_extent is None

        # 2. Run test.
        ClusterShpFom.add_neighbour_extent(_left_cluster, _right_cluster)

        # 3. Verify expectations.
        assert (
            _left_cluster.right_neighbour_extent
            == _right_cluster.left_neighbour_extent
            == _expected_neighbour_extent
        )
