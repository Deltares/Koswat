from pathlib import Path
from typing import Union

import pytest
from shapely.geometry import Point

from koswat.io.koswat_reader_protocol import (
    FileObjectModelProtocol,
    KoswatReaderProtocol,
)
from koswat.io.shp import KoswatShpFom, KoswatShpReader
from tests import test_data
from tests.io import invalid_paths_cases


class TestKoswatShpFom:
    def test_initialize_koswat_shp_fom(self):
        _model = KoswatShpFom()
        assert isinstance(_model, KoswatShpFom)
        assert isinstance(_model, FileObjectModelProtocol)
        assert not _model.is_valid()


class TestKoswatShpReader:
    def test_initialize_koswat_shp_reader(self):
        _reader = KoswatShpReader()
        assert isinstance(_reader, KoswatShpReader)
        assert isinstance(_reader, KoswatReaderProtocol)

    def test_read_given_invalid_file_raises_error(self):
        # 1. Define test data.
        _file = Path() / "not_a_file.shp"
        assert not _file.is_file()
        _reader = KoswatShpReader()
        assert _reader.supports_file(_file)

        # 2. Run test.
        with pytest.raises(FileNotFoundError) as exc_err:
            _reader.read(_file)

        # 3. Verify expectations.
        assert _file.name in str(exc_err.value)

    @pytest.mark.parametrize("shp_file", invalid_paths_cases)
    def test_read_given_invalid_shp_file_raises_error(
        self, shp_file: Union[None, str, Path]
    ):
        # 1. Define test data.
        _reader = KoswatShpReader()
        assert not _reader.supports_file(shp_file)

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            KoswatShpReader().read(shp_file)

        # 3. Verify final expectations.
        assert str(exc_err.value) == "Shp file should be provided"

    def test_given_valid_data_then_returns_data(self):
        # 1. Define test data.
        _test_dir = test_data / "shp_reader" / "Dijkvak"
        _test_file = _test_dir / "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp"
        assert _test_file.is_file()

        # 2. Run test.
        _data = KoswatShpReader().read(_test_file)

        # 3. Verify expectations
        assert isinstance(_data, KoswatShpFom)
        assert isinstance(_data.initial_point, Point)
        assert isinstance(_data.end_point, Point)
        assert _data.is_valid()
