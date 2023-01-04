from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_reader import (
    KoswatSurroundingsCsvReader,
)
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from tests import test_data


class TestKoswatSurroundingsCsvReader:
    def test_initialize(self):
        _csv_reader = KoswatSurroundingsCsvReader()
        assert isinstance(_csv_reader, KoswatSurroundingsCsvReader)
        assert isinstance(_csv_reader, KoswatReaderProtocol)
    
    def test_read_given_valid_file(self):
        # 1. Define test data
        _reader = KoswatSurroundingsCsvReader()
        _test_file = test_data / "csv_reader" / "Omgeving" / "T_10_3_bebouwing_binnendijks.csv"
        assert _test_file.is_file()

        # 2. Run test.
        _csv_fom = _reader.read(_test_file)

        # 3. Verify expectations.
        assert isinstance(_csv_fom, KoswatTrajectSurroundingsCsvFom)
        assert _csv_fom.is_valid()
        