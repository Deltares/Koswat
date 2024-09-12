import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import pytest

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.io.koswat_surroundings_importer import (
    KoswatSurroundingsImporter,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import (
    SurroundingsInfrastructure,
    SurroundingsObstacle,
    SurroundingsWrapper,
)
from tests import get_fixturerequest_case_name, test_data, test_results


@dataclass
class SurroundingsSection:
    """
    Helper class for unittests
    """

    surroundings_database_dir: str


_surroundings_analysis_path = test_data.joinpath("acceptance", "surroundings_analysis")
_surroundings_test_cases = [
    pytest.param(_sap, id=f"Case - {_sap.stem}")
    for _sap in _surroundings_analysis_path.glob("*")
    if _sap.is_dir()
]


class TestKoswatSurroundingsImporter:
    def test_initialize(self):
        _importer = KoswatSurroundingsImporter()
        assert isinstance(_importer, KoswatSurroundingsImporter)
        assert isinstance(_importer, KoswatImporterProtocol)
        assert _importer.traject_loc_shp_file == None
        assert _importer.selected_locations == []

    def test_import_from_raises_when_from_path_not_given(self):
        # 1. Define test data.
        _importer = KoswatSurroundingsImporter()
        _expected_error = "No surroundings csv directory path given."
        _surroundings_section = SurroundingsSection(surroundings_database_dir=None)

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _importer.import_from(_surroundings_section)

        # 3. Verify expectations.
        assert _expected_error == str(exc_err.value)

    def test_import_from_raises_when_traject_loc_shp_file_not_given(self):
        # 1. Define test data.
        _importer = KoswatSurroundingsImporter()
        _expected_error = "No traject shp file path given."
        _surroundings_section = SurroundingsSection(surroundings_database_dir=Path())

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _importer.import_from(_surroundings_section)

        # 3. Verify expectations.
        assert _expected_error == str(exc_err.value)

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
        # traject's surroundings are avaiable in said dir.
        yield SurroundingsSectionFom(
            surroundings_database_dir=_temp_dir.parent,
            constructieafstand=50,
            constructieovergang=10,
            buitendijks=False,
            bebouwing=True,
            spoorwegen=False,
            water=False,
        )

        # Remove the temporary directory.
        shutil.rmtree(_temp_dir)

    def test_given_valid_surroundings_file_when_import_from_returns_surrounding_wrapper(
        self, surroundings_section_fom_fixture: SurroundingsSectionFom
    ):
        # 1. Define test data.
        assert isinstance(surroundings_section_fom_fixture, SurroundingsSectionFom)

        _shp_file = test_data.joinpath("acceptance", "shp", "dike_locations.shp")
        assert _shp_file.is_file()

        _importer = KoswatSurroundingsImporter()
        _importer.traject_loc_shp_file = _shp_file
        _importer.selected_locations = [
            # For traject 10-1
            "10-1-3-C-1-D-1",
            "10-1-3-C-1-A",
            # For traject 10-2
            "10-1-4-C-1-B",
            "10-1-4-B-1-B-1",
            # For traject 10-3
            "10-1-2-A-1-A",
            "10-1-1-A-1-A",
        ]

        # 2. Run test.
        _surroundings_wrapper_list = _importer.import_from(
            surroundings_section_fom_fixture
        )

        # 3. Verify expectations (specific for the caes present in the test data).
        assert len(_surroundings_wrapper_list) == 2

        def check_surroundings(
            surrounding_property: KoswatSurroundingsProtocol,
            expected_type: type[KoswatSurroundingsProtocol],
        ):
            assert isinstance(surrounding_property, KoswatSurroundingsProtocol)
            assert isinstance(surrounding_property, expected_type)
            assert any(surrounding_property.points)

        for _sw in _surroundings_wrapper_list:
            assert isinstance(_sw, SurroundingsWrapper)
            check_surroundings(_sw.buildings_polderside, SurroundingsObstacle)
            if _sw.traject != "10-2":
                check_surroundings(_sw.railways_polderside, SurroundingsObstacle)
            check_surroundings(_sw.waters_polderside, SurroundingsObstacle)
            check_surroundings(_sw.roads_class_2_polderside, SurroundingsInfrastructure)
            check_surroundings(_sw.roads_class_7_polderside, SurroundingsInfrastructure)
            check_surroundings(
                _sw.roads_class_24_polderside, SurroundingsInfrastructure
            )
            check_surroundings(
                _sw.roads_class_47_polderside, SurroundingsInfrastructure
            )
            check_surroundings(
                _sw.roads_class_unknown_polderside, SurroundingsInfrastructure
            )

    @pytest.mark.parametrize(
        "surroundings_path",
        [
            pytest.param(_sap, id=f"Case: {_sap.stem}")
            for _sap in _surroundings_analysis_path.glob("*")
            if _sap.is_dir()
        ],
    )
    def test_given_valid_surroundings_dir_when__csv_dir_to_fom_returns_surrounding_wrapper(
        self, surroundings_path: Path
    ):
        # 1. Define test data.
        assert surroundings_path.exists()

        # 2. Run test.
        _surroundings_wrapper_fom = KoswatSurroundingsImporter()._csv_dir_to_fom(
            surroundings_path
        )

        # 3. Verify expectations.
        assert isinstance(
            _surroundings_wrapper_fom, KoswatTrajectSurroundingsWrapperCsvFom
        )
