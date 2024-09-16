import shutil
from typing import Callable, Iterator

import pytest
from shapely.geometry import Point

from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.io.koswat_surroundings_importer import (
    KoswatSurroundingsWrapperCollectionBuilder,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from tests import get_test_results_dir, test_data, test_results


class TestSurroundingsWrapper:
    def test_initialize(self):
        _surroundings = SurroundingsWrapper()
        assert isinstance(_surroundings, SurroundingsWrapper)
        assert isinstance(
            _surroundings.obstacle_surroundings_wrapper, ObstacleSurroundingsWrapper
        )
        assert isinstance(
            _surroundings.infrastructure_surroundings_wrapper,
            InfrastructureSurroundingsWrapper,
        )

    # @pytest.mark.parametrize(
    #     "obstacle_name",
    #     [pytest.param("buildings"), pytest.param("railways"), pytest.param("waters")],
    # )
    # def test_set_obstacles_polderside(
    #     self,
    #     obstacle_name: str,
    #     distances_to_surrounding_point_builder: Callable[
    #         [Point, list[float]], PointSurroundings
    #     ],
    # ):
    #     # 1. Define test data.
    #     _obstacles_polderside = SurroundingsObstacle()
    #     _locations = [
    #         Point(4.2, 2.4),
    #         Point(4.2, 4.2),
    #         Point(2.4, 2.4),
    #     ]
    #     _obstacles_polderside.points = list(
    #         map(distances_to_surrounding_point_builder, _locations, [[0], [2], [24]])
    #     )

    #     # 2. Run test.
    #     _surroundings = SurroundingsWrapper(
    #         **{
    #             f"apply_{obstacle_name}": True,
    #             f"{obstacle_name}_polderside": _obstacles_polderside,
    #         }
    #     )

    #     # 3. Verify expectations.
    #     assert isinstance(_surroundings.buildings_polderside, SurroundingsObstacle)

    #     # Doing it like this because sorting requires setting up a sorting key.
    #     _explored = []
    #     assert len(set(_surroundings.obstacle_locations)) == len(_locations)
    #     for _sp in _surroundings.obstacle_locations:
    #         assert _sp.location in _locations
    #         # Check there are no repeated points, thus invalidating the test.
    #         assert _sp not in _explored
    #         _explored.append(_sp)

    @pytest.fixture(name="surroundings_with_obstacle_builder")
    def _get_surroundings_with_obstacle_builder_fixture(
        self,
        distances_to_surrounding_point_builder: Callable[
            [Point, list[float]], PointSurroundings
        ],
    ) -> Iterator[Callable[[list[Point], list[list[float]]], SurroundingsWrapper]]:
        def create_surroundings_wrapper(
            point_list: list[Point], distance_list: list[float]
        ):
            # _buildings_polderside = SurroundingsObstacle()
            # _railways_polderside = SurroundingsObstacle()
            # _waters_polderside = SurroundingsObstacle()
            # _buildings_polderside.points = list(
            #     map(
            #         distances_to_surrounding_point_builder, point_list, distance_list[0]
            #     )
            # )
            # _railways_polderside.points = list(
            #     map(
            #         distances_to_surrounding_point_builder, point_list, distance_list[1]
            #     )
            # )
            # _waters_polderside.points = list(
            #     map(
            #         distances_to_surrounding_point_builder, point_list, distance_list[2]
            #     )
            # )

            # Yield wrapper
            return SurroundingsWrapper()

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

    @pytest.mark.parametrize(
        "obstacles_distance_list",
        [
            pytest.param([24], id="Surroundings WITH obstacles at distance 24"),
            pytest.param([], id="Surroundings WITHOUT obstacles"),
        ],
    )
    def test_when_get_locations_at_safe_distance_given_safe_obstacles_returns_surrounding_point(
        self,
        obstacles_distance_list: list[float],
        surroundings_with_obstacle_builder: Callable[
            [list[Point], list[list[float]]], SurroundingsWrapper
        ],
    ):
        # 1. Define test data.
        _safe_distance = min(obstacles_distance_list, default=0) - 1
        _wrapper = surroundings_with_obstacle_builder(
            [Point(2.4, 2.4)], [[obstacles_distance_list]] * 3
        )

        # 2. Run test.
        _classified_surroundings = _wrapper.get_locations_at_safe_distance(
            _safe_distance
        )

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, list)
        assert len(_classified_surroundings) == 1
        assert _classified_surroundings[0] == _wrapper.obstacle_locations[0]

    def test_when_get_locations_after_distance_given_unsafe_obstacles_returns_nothing(
        self,
        surroundings_with_obstacle_builder: Callable[
            [list[Point], list[list[float]]], SurroundingsWrapper
        ],
    ):
        # 1. Define test data.
        _obstacles_distance_list = [24]
        _wrapper = surroundings_with_obstacle_builder(
            [Point(2.4, 2.4)], [[_obstacles_distance_list]] * 3
        )

        # 2. Run test.
        _classified_surroundings = _wrapper.get_locations_at_safe_distance(
            min(_obstacles_distance_list) + 1
        )

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, list)
        assert not any(_classified_surroundings)

    @pytest.fixture(name="surroundings_wrapper_with_infrastructure")
    def _get_surroundings_wrapper_with_infrastructure_fixture(
        self, request: pytest.FixtureRequest
    ) -> Iterator[SurroundingsWrapper]:
        # Shp locations file
        _shp_file = test_data.joinpath("acceptance", "shp", "dike_locations.shp")
        assert _shp_file.is_file()

        # Surroundings directory
        _surroundings_analysis_path = test_data.joinpath(
            "acceptance", "surroundings_analysis", "10_1"
        )
        assert _surroundings_analysis_path.is_dir()

        # Create a dummy dir to avoid importing unnecessary data.
        _dir_name = get_test_results_dir(request)
        _temp_dir = test_results.joinpath(_dir_name, "10_1")
        if _temp_dir.exists():
            shutil.rmtree(_temp_dir)
        shutil.copytree(_surroundings_analysis_path, _temp_dir)

        # Generate surroundings section File Object Model.
        _surroundings_settings = SurroundingsSectionFom(
            surroundings_database_dir=_temp_dir.parent,
            constructieafstand=float("nan"),
            constructieovergang=float("nan"),
            buitendijks=False,
            bebouwing=False,
            spoorwegen=False,
            water=False,
        )

        # Generate wrapper
        _importer = KoswatSurroundingsWrapperCollectionBuilder()
        _importer.selected_locations = "10-1-3-C-1-D-1"
        _importer.traject_loc_shp_file = _shp_file
        _surroundings_wrapper_list = _importer.import_from(_surroundings_settings)
        assert len(_surroundings_wrapper_list) == 1

        # Yield result
        yield _surroundings_wrapper_list[0]

        # Remove temp dir
        shutil.rmtree(_temp_dir)

    def test_get_infrastructure_collection_given_acceptance_case_returns_dict(
        self, surroundings_wrapper_with_infrastructure: SurroundingsWrapper
    ):
        # 1. Define test data
        assert isinstance(surroundings_wrapper_with_infrastructure, SurroundingsWrapper)

        # 2. Run test.
        _infra_matrix = (
            surroundings_wrapper_with_infrastructure.infrastructure_collection
        )

        # 3. Verify expectations.
        assert isinstance(_infra_matrix, dict)
        assert any(_infra_matrix.items())
        assert all(
            map(
                lambda _si: isinstance(_si, SurroundingsInfrastructure),
                _infra_matrix.values(),
            )
        )
