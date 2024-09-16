import shutil
from typing import Callable, Iterator

import pytest
from shapely.geometry import Point

from koswat.configuration.io.ini.koswat_general_ini_fom import (
    InfrastructureSectionFom,
    SurroundingsSectionFom,
)
from koswat.configuration.io.koswat_surroundings_importer import (
    SurroundingsWrapperCollectionImporter,
)
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
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

    @pytest.fixture(name="acceptance_surroundings_wrapper_fixture")
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

        # Generate Infrastructures section file model
        _infrastructure_settings = InfrastructureSectionFom(
            infrastructuur=True,
            opslagfactor_wegen=SurtaxFactorEnum.NORMAAL,
            infrakosten_0dh=InfraCostsEnum.GEEN,
            buffer_buitendijks=0.24,
            wegen_klasse2_breedte=1,
            wegen_klasse7_breedte=2,
            wegen_klasse24_breedte=3,
            wegen_klasse47_breedte=4,
            wegen_onbekend_breedte=5,
        )

        # Generate wrapper
        _importer = SurroundingsWrapperCollectionImporter(
            infrastructure_section_fom=_infrastructure_settings,
            surroundings_section_fom=_surroundings_settings,
            selected_locations=["10-1-3-c-1-d-1"],
            traject_loc_shp_file=_shp_file,
        )
        _surroundings_wrapper_list = _importer.build()
        assert len(_surroundings_wrapper_list) == 1

        # Yield result
        yield _surroundings_wrapper_list[0]

        # Remove temp dir
        shutil.rmtree(_temp_dir)

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
        pytest.fail("Needs to be moved to `TestObstacleSurroundingsWrapper`.")
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
