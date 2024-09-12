from math import dist
from typing import Callable, Iterator

import pytest
from shapely.geometry import Point

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.wrapper.surroundings_wrapper import (
    SurroundingsInfrastructure,
    SurroundingsObstacle,
    SurroundingsWrapper,
)


class TestSurroundingsWrapper:
    def test_initialize(self):
        _surroundings = SurroundingsWrapper()
        assert isinstance(_surroundings, SurroundingsWrapper)
        assert any(_surroundings.surroundings_collection)
        assert all(
            isinstance(_s, SurroundingsInfrastructure)
            for _s in _surroundings.surroundings_collection
        )
        assert not _surroundings.obstacle_locations

        # Mapped as obstacle
        assert isinstance(_surroundings.buildings_polderside, SurroundingsObstacle)
        assert isinstance(_surroundings.railways_polderside, SurroundingsObstacle)
        assert isinstance(_surroundings.waters_polderside, SurroundingsObstacle)

        # Mapped as infrastructure
        assert isinstance(
            _surroundings.roads_class_2_polderside, SurroundingsInfrastructure
        )
        assert isinstance(
            _surroundings.roads_class_7_polderside, SurroundingsInfrastructure
        )
        assert isinstance(
            _surroundings.roads_class_24_polderside, SurroundingsInfrastructure
        )
        assert isinstance(
            _surroundings.roads_class_47_polderside, SurroundingsInfrastructure
        )
        assert isinstance(
            _surroundings.roads_class_unknown_polderside,
            SurroundingsInfrastructure,
        )

        # Unmapped (not supported yet)
        # Obstacles
        assert not _surroundings.buildings_dikeside
        assert not _surroundings.railways_dikeside
        assert not _surroundings.waters_dikeside
        # Infrastructures
        assert not _surroundings.roads_class_2_dikeside
        assert not _surroundings.roads_class_7_dikeside
        assert not _surroundings.roads_class_24_dikeside
        assert not _surroundings.roads_class_47_dikeside
        assert not _surroundings.roads_class_unknown_dikeside

    def _to_surrounding_point(
        self, location: Point, distances_list: list[float]
    ) -> PointSurroundings:
        return PointSurroundings(
            location=location, surroundings_matrix={_d: 1 for _d in distances_list}
        )

    @pytest.mark.parametrize(
        "obstacle_name",
        [pytest.param("buildings"), pytest.param("railways"), pytest.param("waters")],
    )
    def test_set_obstacles_polderside(self, obstacle_name: str):
        # 1. Define test data.
        _obstacles_polderside = SurroundingsObstacle()
        _locations = [
            Point(4.2, 2.4),
            Point(4.2, 4.2),
            Point(2.4, 2.4),
        ]
        _obstacles_polderside.points = list(
            map(self._to_surrounding_point, _locations, [[0], [2], [24]])
        )

        # 2. Run test.
        _surroundings = SurroundingsWrapper(
            **{
                f"apply_{obstacle_name}": True,
                f"{obstacle_name}_polderside": _obstacles_polderside,
            }
        )

        # 3. Verify expectations.
        assert isinstance(_surroundings.buildings_polderside, SurroundingsObstacle)

        # Doing it like this because sorting requires setting up a sorting key.
        _explored = []
        assert len(set(_surroundings.obstacle_locations)) == len(_locations)
        for _sp in _surroundings.obstacle_locations:
            assert _sp.location in _locations
            # Check there are no repeated points, thus invalidating the test.
            assert _sp not in _explored
            _explored.append(_sp)

    @pytest.fixture(name="surroundings_with_obstacle_builder")
    def _get_surroundings_with_obstacle_builder_fixture(
        self,
    ) -> Iterator[Callable[[list[Point], list[list[float]]], SurroundingsWrapper]]:
        def create_surroundings_wrapper(
            point_list: list[Point], distance_list: list[float]
        ):
            _buildings_polderside = SurroundingsObstacle()
            _railways_polderside = SurroundingsObstacle()
            _waters_polderside = SurroundingsObstacle()
            _buildings_polderside.points = list(
                map(self._to_surrounding_point, point_list, distance_list[0])
            )
            _railways_polderside.points = list(
                map(self._to_surrounding_point, point_list, distance_list[1])
            )
            _waters_polderside.points = list(
                map(self._to_surrounding_point, point_list, distance_list[2])
            )

            # Yield wrapper
            return SurroundingsWrapper(
                buildings_polderside=_buildings_polderside,
                railways_polderside=_railways_polderside,
                waters_polderside=_waters_polderside,
                apply_buildings=True,
                apply_railways=True,
                apply_waters=False,
            )

        yield create_surroundings_wrapper

    def test_get_obstacle_locations(
        self, surroundings_with_obstacle_builder: SurroundingsWrapper
    ):
        # 1. Define test data.
        _locations = [
            Point(4.2, 2.4),
            Point(4.2, 4.2),
            Point(2.4, 2.4),
        ]
        _distances = [
            [[], [], []],
            [[], [], []],
            [[], [], []],
        ]
        _surroundings = surroundings_with_obstacle_builder(_locations, _distances)
        assert isinstance(_surroundings, SurroundingsWrapper)

        # 2. Run test.
        _obstacle_locations = _surroundings.obstacle_locations

        # 3. Verify expectations.
        # Doing it like this because sorting requires setting up a sorting key.
        assert len(_obstacle_locations) == len(_locations)
        assert all(isinstance(_ol, PointSurroundings) for _ol in _obstacle_locations)

        _explored = []
        for _ol_point in _obstacle_locations:
            assert _ol_point.location in _locations
            # Check there are no repeated points, thus invalidating the test.
            assert _ol_point not in _explored
            _explored.append(_ol_point)

    def test_get_safe_locations(
        self,
        surroundings_with_obstacle_builder: Callable[
            [list[Point], list[list[float]]], SurroundingsWrapper
        ],
    ):
        # 1. Define test data.
        _locations = [
            Point(4.2, 2.4),
            Point(4.2, 4.2),
            Point(2.4, 2.4),
        ]
        _distances = [
            [[], [20, 50], [10, 50]],
            [[], [15], [20]],
            [[5, 100], [5, 100], [5, 100]],
        ]
        _surroundings = surroundings_with_obstacle_builder(_locations, _distances)
        assert isinstance(_surroundings, SurroundingsWrapper)

        # 2. Run test.
        _safe_points = _surroundings.get_locations_at_safe_distance(12)

        # 3. Verify expectations.
        # Doing it like this because sorting requires setting up a sorting key.
        assert all(map(lambda x: isinstance(x, PointSurroundings), _safe_points))

        _explored = []
        assert len(set(_safe_points)) == len(_locations)
        for _sp in _safe_points:
            assert _sp.location in _locations
            # Check there are no repeated points, thus invalidating the test.
            assert _sp not in _explored
            _explored.append(_sp)
