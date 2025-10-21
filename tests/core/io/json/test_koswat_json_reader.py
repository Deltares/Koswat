from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class TestKoswatJsonReader:
    def test_koswat_json_reader_init(self):
        _json_reader = KoswatJsonReader()
        assert isinstance(_json_reader, KoswatJsonReader)
        assert isinstance(_json_reader, KoswatReaderProtocol)
