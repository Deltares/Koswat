from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from tests import test_data_acceptance


class TestKoswatJsonReader:
    def test_koswat_json_reader_init(self):
        _json_reader = KoswatJsonReader()
        assert isinstance(_json_reader, KoswatJsonReader)
        assert isinstance(_json_reader, KoswatReaderProtocol)

    def test_when_read_given_valid_json_then_returns_koswat_json_fom(self):
        # 1. Define test data.
        _json_file = test_data_acceptance.joinpath("koswat_general.json")
        assert _json_file.is_file()

        # 2. Run test.
        _json_reader = KoswatJsonReader()
        _json_fom = _json_reader.read(_json_file)

        # 3. Verify expectations.
        assert _json_fom.file_path == _json_file
        assert isinstance(_json_fom.content, dict)
