from dataclasses import dataclass
from pathlib import Path

import pytest

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.io.koswat_surroundings_importer import (
    KoswatSurroundingsImporter,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from tests import test_data


@dataclass
class SurroundingsSection:
    """
    Helper class for unittests
    """

    surroundings_database_dir: str


_surroundings_analysis_path = test_data.joinpath("acceptance", "surroundings_analysis")


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

    @pytest.mark.parametrize(
        "surroundings_path",
        [
            pytest.param(_sap, id=f"Case: {_sap.stem}")
            for _sap in _surroundings_analysis_path.glob("*")
            if _sap.is_dir()
        ],
    )
    def test_given_valid_surroundings_file_when_import_from_returns_surrounding_wrapper(
        self, surroundings_path: Path
    ):
        # 1. Define test data.
        assert surroundings_path.exists()
        _surroundings_section = SurroundingsSection(
            surroundings_database_dir=surroundings_path.parent
        )

        _shp_file = test_data.joinpath("acceptance", "shp", "dike_locations.shp")
        assert _shp_file.is_file()

        _importer = KoswatSurroundingsImporter()
        _importer.traject_loc_shp_file = _shp_file
        _importer.selected_locations = [
            "10-1-3-C-1-D-1",
            "10-1-4-C-1-B",
            "10-1-3-C-1-A",
        ]
        # 2. Run test.
        _surroundings_wrapper_list = _importer.import_from(_surroundings_section)

        # 3. Verify expectations.
        assert len(_surroundings_wrapper_list) == len(_importer.selected_locations)
        assert all(
            isinstance(_sw, SurroundingsWrapper) for _sw in _surroundings_wrapper_list
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
