import pytest

from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_reader import (
    KoswatDikeLocationsListShpReader,
)
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from tests import test_data

valid_shp_file = test_data / "acceptance" / "shp" / "dike_locations.shp"


class TestKoswatDikeLocationsListShpReader:
    def test_initialize(self):
        _shp_reader = KoswatDikeLocationsListShpReader()
        assert isinstance(_shp_reader, KoswatDikeLocationsListShpReader)
        assert isinstance(_shp_reader, KoswatReaderProtocol)
        assert _shp_reader.selected_locations == []

    def test_read_given_valid_file_and_selected_locations(self):
        # 1. Define test data
        _shp_reader = KoswatDikeLocationsListShpReader()
        _shp_reader.selected_locations = ["10-1-1-A-1-A"]
        assert valid_shp_file.is_file()

        # 2. Run test.
        _list_fom = _shp_reader.read(valid_shp_file)

        # 3. Verify final expectations.
        assert any(_list_fom)
        assert all(isinstance(_fom, KoswatDikeLocationsShpFom) for _fom in _list_fom)

    def test_read_given_invalid_file_raises_value_error(self):
        # 1. Define test data
        _shp_reader = KoswatDikeLocationsListShpReader()
        _expected_error = "Shp file should be provided"
        _test_file = valid_shp_file.with_suffix(".notshp")

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _shp_reader.read(_test_file)

        # 3. Verify expectations
        assert _expected_error == str(exc_err.value)

    def test_read_given_valid_file_and_no_selected_locations(self):
        # 1. Define test data
        _shp_reader = KoswatDikeLocationsListShpReader()
        assert valid_shp_file.is_file()

        # 2. Run test.
        _list_fom = _shp_reader.read(valid_shp_file)

        # 3. Verify final expectations.
        assert not _list_fom
