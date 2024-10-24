import shutil
from typing import Iterator

import pytest

from koswat.configuration.io.ini.koswat_general_ini_fom import (
    InfrastructureSectionFom,
    SurroundingsSectionFom,
)
from koswat.configuration.io.surroundings_wrapper_collection_importer import (
    SurroundingsWrapperCollectionImporter,
)
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
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
            bebouwing=True,
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
            selected_locations=["10-1-3-C-1-D-1"],
            traject_loc_shp_file=_shp_file,
        )
        _surroundings_wrapper_list = _importer.build()
        assert len(_surroundings_wrapper_list) == 1

        # Yield result
        yield _surroundings_wrapper_list[0]

        # Remove temp dir
        shutil.rmtree(_temp_dir)

    def test_get_wrapper_with_acceptance_case(
        self, acceptance_surroundings_wrapper_fixture: SurroundingsWrapper
    ):
        _wrapper = acceptance_surroundings_wrapper_fixture
        assert isinstance(_wrapper, SurroundingsWrapper)

        # Obstacles
        _obs = _wrapper.obstacle_surroundings_wrapper
        assert isinstance(_obs, ObstacleSurroundingsWrapper)
        assert any(_obs.surroundings_collection)
        assert any(_obs.obstacle_locations)

        # Infra
        _infra = _wrapper.infrastructure_surroundings_wrapper
        assert isinstance(_infra, InfrastructureSurroundingsWrapper)
        assert any(_infra.surroundings_collection)
        assert all(
            _sw.infrastructure_name != ""
            for _sw in _infra.surroundings_collection.values()
        )
