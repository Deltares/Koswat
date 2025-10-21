from koswat.configuration.io.json.koswat_input_profile_json_fom import (
    KoswatInputProfileJsonFom,
)
from koswat.configuration.io.json.koswat_input_profile_json_reader import (
    KoswatInputProfileJsonReader,
)
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from tests import test_data_acceptance


class TestKoswatInputProfileJsonReader:
    def test_initialize(self):
        _reader = KoswatInputProfileJsonReader()
        assert isinstance(_reader, KoswatInputProfileJsonReader)
        assert isinstance(_reader, KoswatReaderProtocol)

    def test_given_valid_file_read(self):
        # 1. Define test data
        _reader = KoswatInputProfileJsonReader()
        _test_file = test_data_acceptance.joinpath(
            "json", "dikesection_input", "10-1-1-A-1-A.json"
        )
        assert _test_file.is_file()

        # 2. Run test.
        _json_fom = _reader.read(_test_file)

        # 3. Verify expectations.
        assert isinstance(_json_fom, KoswatInputProfileJsonFom)
        assert _json_fom.is_valid()
