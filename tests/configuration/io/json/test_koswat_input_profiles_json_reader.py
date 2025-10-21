from koswat.configuration.io.csv.koswat_input_profiles_csv_fom import (
    KoswatInputProfilesCsvFom,
)
from koswat.configuration.io.csv.koswat_input_profiles_csv_reader import (
    KoswatInputProfilesCsvReader,
)
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from tests import test_data


class TestKoswatInputProfilesCsvReader:
    def test_initialize(self):
        _reader = KoswatInputProfilesCsvReader()
        assert isinstance(_reader, KoswatInputProfilesCsvReader)
        assert isinstance(_reader, KoswatReaderProtocol)

    def test_given_valid_file_read(self):
        # 1. Define test data
        _reader = KoswatInputProfilesCsvReader()
        _test_file = test_data / "acceptance" / "csv" / "dike_input_profiles.csv"
        assert _test_file.is_file()

        # 2. Run test.
        _csv_fom = _reader.read(_test_file)

        # 3. Verify expectations.
        assert isinstance(_csv_fom, KoswatInputProfilesCsvFom)
        assert _csv_fom.is_valid()
