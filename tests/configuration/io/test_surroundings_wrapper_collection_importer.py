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
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from tests import get_fixturerequest_case_name, test_data, test_results

_surroundings_analysis_path = test_data.joinpath("acceptance", "surroundings_analysis")
_surroundings_test_cases = [
    pytest.param(_sap, id=f"Case - {_sap.stem}")
    for _sap in _surroundings_analysis_path.glob("*")
    if _sap.is_dir()
]


class TestSurroundingsWrapperCollectionImporter:
    def test_initialize(self):
        # !. Define dummy importer.
        _importer = SurroundingsWrapperCollectionImporter(
            infrastructure_section_fom=None,
            surroundings_section_fom=None,
            traject_loc_shp_file=None,
            selected_locations=[],
        )

        # 2. Validate expectations.
        assert isinstance(_importer, SurroundingsWrapperCollectionImporter)
        assert isinstance(_importer, BuilderProtocol)
        assert not _importer.traject_loc_shp_file
        assert not _importer.selected_locations
        assert not _importer.surroundings_section_fom
        assert not _importer.infrastructure_section_fom

    @pytest.fixture(
        name="surroundings_section_fom_fixture",
        params=[_stc.values for _stc in _surroundings_test_cases],
        ids=[_stc.id for _stc in _surroundings_test_cases],
    )
    def _get_surroundings_section_fom_fixture(
        self, request: pytest.FixtureRequest
    ) -> Iterator[SurroundingsSectionFom]:

        # Create a copy of the directory in a temporary location
        _case_name = get_fixturerequest_case_name(request)
        _surroundings_path = request.param[0]
        _temp_dir = test_results.joinpath(_case_name, _surroundings_path.stem)
        if _temp_dir.parent.exists():
            shutil.rmtree(_temp_dir.parent)
        shutil.copytree(_surroundings_path, _temp_dir)

        # Yield the surroundings section.
        # Remember! The database dir is the parent as in theory more
        # traject's surroundings are available in said dir.
        yield SurroundingsSectionFom(
            surroundings_database_dir=_temp_dir.parent,
            construction_distance=50,
            construction_buffer=10,
            waterside=True,
            buildings=True,
            railways=True,
            waters=True,
        )

        # Remove the temporary directory.
        shutil.rmtree(_temp_dir)

    @pytest.fixture(name="infrastructure_section_fom_fixture")
    def _get_infrastructure_section_fom(self) -> Iterator[InfrastructureSectionFom]:
        yield InfrastructureSectionFom(
            infrastructure=True,
            surtax_factor_roads=SurtaxFactorEnum.NORMAAL,
            infrastructure_costs_0dh=InfraCostsEnum.GEEN,
            buffer_waterside=0.42,
            roads_class2_width=2.4,
            roads_class24_width=4.2,
            roads_class47_width=24,
            roads_class7_width=42,
            roads_unknown_width=0.67,
        )

    def test_given_valid_surroundings_path_when_import_from_returns_surrounding_wrapper(
        self,
        surroundings_section_fom_fixture: SurroundingsSectionFom,
        infrastructure_section_fom_fixture: InfrastructureSectionFom,
    ):
        # 1. Define test data.
        assert isinstance(surroundings_section_fom_fixture, SurroundingsSectionFom)

        _shp_file = test_data.joinpath("acceptance", "shp", "dike_locations.shp")
        assert _shp_file.is_file()

        _builder = SurroundingsWrapperCollectionImporter(
            surroundings_section_fom=surroundings_section_fom_fixture,
            infrastructure_section_fom=infrastructure_section_fom_fixture,
            traject_loc_shp_file=_shp_file,
            selected_locations=[
                # For traject 10-1
                "10-1-3-C-1-D-1",
                "10-1-3-C-1-A",
                # For traject 10-2
                "10-1-4-C-1-B",
                "10-1-4-B-1-B-1",
                # For traject 10-3
                "10-1-2-A-1-A",
                "10-1-1-A-1-A",
            ],
        )

        # 2. Run test.
        _surroundings_wrapper_list = _builder.build()

        # 3. Verify expectations (specific for the case present in the test data).
        assert len(_surroundings_wrapper_list) == 2
        for _sw in _surroundings_wrapper_list:
            assert isinstance(_sw, SurroundingsWrapper)

            # Obstacle Surroundings
            assert isinstance(
                _sw.obstacle_surroundings_wrapper, ObstacleSurroundingsWrapper
            )
            assert any(_sw.obstacle_surroundings_wrapper.obstacle_locations)

            # Infrastructure Surroundings
            assert isinstance(
                _sw.infrastructure_surroundings_wrapper,
                InfrastructureSurroundingsWrapper,
            )
            assert any(
                _sw.infrastructure_surroundings_wrapper.roads_class_2_polderside.points
            )
            assert any(
                _sw.infrastructure_surroundings_wrapper.roads_class_7_polderside.points
            )
            assert any(
                _sw.infrastructure_surroundings_wrapper.roads_class_24_polderside.points
            )
            assert any(
                _sw.infrastructure_surroundings_wrapper.roads_class_47_polderside.points
            )
