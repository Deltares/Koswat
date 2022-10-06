from pathlib import Path
from typing import Union

import pytest

from koswat.io.koswat_csv_fom import KoswatCsvFom
from koswat.io.koswat_csv_reader import KoswatCsvReader
from koswat.io.koswat_reader_protocol import KoswatReaderProtocol
from tests import test_data


class TestKoswatCsvReader:
    def test_initialize_csv_reader(self):
        _csv_reader = KoswatCsvReader()
        assert isinstance(_csv_reader, KoswatCsvReader)
        assert isinstance(_csv_reader, KoswatReaderProtocol)
        assert _csv_reader.separator == ";"

    def test_read_given_valid_file_returns_fom(self):
        # 1. Define test data.
        _test_data = test_data / "csv_reader" / "Omgeving"
        _test_file = _test_data / "T_10_3_bebouwing_binnendijks.csv"
        assert _test_file.is_file()
        _reader = KoswatCsvReader()
        assert _reader.supports_file(_test_file)

        # 2. Run test
        _csv_fom = _reader.read(_test_file)

        # 3. Verify expectations.
        assert isinstance(_csv_fom, KoswatCsvFom)
        assert _csv_fom.is_valid()

    def test_read_given_invalid_file_raises_error(self):
        # 1. Define test data.
        _file = Path() / "not_a_file.csv"
        assert not _file.is_file()
        _reader = KoswatCsvReader()
        assert _reader.supports_file(_file)

        # 2. Run test.
        with pytest.raises(FileNotFoundError) as exc_err:
            _reader.read(_file)

        # 3. Verify expectations.
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
        # 1. Define test data.
        _reader = KoswatCsvReader()
        assert not _reader.supports_file(shp_file)

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            KoswatCsvReader().read(shp_file)

        # 3. Verify final expectations.
        assert str(exc_err.value) == "Csv file should be provided"
