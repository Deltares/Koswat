from pathlib import Path
from typing import Union

import pytest

from koswat.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.io.koswat_shp_reader import KoswatShpReader
from tests import test_data


class TestKoswatShpReader:
    def test_initialize_koswat_shp_reader(self):
        _reader = KoswatShpReader()
        assert isinstance(_reader, KoswatShpReader)
        assert isinstance(_reader, KoswatReaderProtocol)

    def test_read_given_invalid_file_raises_error(self):
        _file = Path() / "not_a_file.shp"
        assert not _file.is_file()
        with pytest.raises(FileNotFoundError) as exc_err:
            KoswatShpReader().read(_file)

        assert _file.name in str(exc_err.value)

    @pytest.mark.parametrize(
        "shp_file",
        [
            pytest.param(None, id="None given"),
            pytest.param("", id="Empty string given"),
            pytest.param("not\\a\\path", id="Path as string"),
            pytest.param(Path() / "not_a_valid_file", id="Wrong extension"),
        ],
    )
    def test_read_given_invalid_shp_file_raises_error(
        self, shp_file: Union[None, str, Path]
    ):
        with pytest.raises(ValueError) as exc_err:
            KoswatShpReader().read(shp_file)
        assert str(exc_err.value) == "Shp file should be provided"

    def test_given_valid_data_then_returns_data(self):
        # 1. Define test data.
        _test_dir = test_data / "shp_reader" / "Dijkvak"
        _test_file = _test_dir / "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp"
        assert _test_file.is_file()

        # 2. Run test.
        _data = KoswatShpReader().read(_test_file)

        # 3. Verify expectations
        assert _data is not None
