from shapely import Point

from koswat.cost_report.io.summary.summary_locations.cluster_shp_fom import (
    ClusterShpFom,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class TestClusterShapeFom:
    def test_points_with_neighbour_extent_without_neighbours(self):
        # 1. Prepare test data.
        _first_point = Point(10, 10)
        _last_point = Point(20, 20)
        _cluster = ClusterShpFom(
            locations=[
                StrategyLocationReinforcement(
                    location=PointSurroundings(location=_first_point)
                ),
                StrategyLocationReinforcement(
                    location=PointSurroundings(location=_last_point)
                ),
            ],
            reinforced_profile=None,
        )
        assert _cluster.left_neighbour_extent is None
        assert _cluster.right_neighbour_extent is None

        # 2. Run test.
        _points = _cluster.points_with_neighbour_extent

        # 3. Verify expectations.
        assert _points == [_first_point, _last_point]

    def test_points_with_neighbour_extent_with_neighbours(self):
        # 1. Prepare test data.
        _left_extent = Point(5, 5)
        _first_point = Point(10, 10)
        _last_point = Point(20, 20)
        _right_extent = Point(25, 25)

        _cluster = ClusterShpFom(
            locations=[
                StrategyLocationReinforcement(PointSurroundings(location=_first_point)),
                StrategyLocationReinforcement(PointSurroundings(location=_last_point)),
            ],
            reinforced_profile=None,
            left_neighbour_extent=_left_extent,
            right_neighbour_extent=_right_extent,
        )

        # 2. Run test.
        _points = _cluster.points_with_neighbour_extent

        # 3. Verify expectations.
        assert _points == [_left_extent, _first_point, _last_point, _right_extent]

    def test_add_neighbour_extent(self):
        # 1. Prepare test data.
        _left_first_point = Point(-99, -99)
        _left_last_point = Point(20, 20)
        _right_first_point = Point(30, 30)
        _right_last_point = Point(99, 99)

        _expected_neighbour_extent = Point(25, 25)

        _left_cluster = ClusterShpFom(
            locations=[
                StrategyLocationReinforcement(
                    location=PointSurroundings(location=_left_first_point)
                ),
                StrategyLocationReinforcement(
                    location=PointSurroundings(location=_left_last_point)
                ),
            ],
            reinforced_profile=None,
        )
        _right_cluster = ClusterShpFom(
            locations=[
                StrategyLocationReinforcement(
                    location=PointSurroundings(location=_right_first_point)
                ),
                StrategyLocationReinforcement(
                    location=PointSurroundings(location=_right_last_point)
                ),
            ],
            reinforced_profile=None,
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
