from koswat.core.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol


class TestKoswatIniReader:
    def test_koswat_ini_reader_init(self):
        _ini_reader = KoswatIniReader()
        assert isinstance(_ini_reader, KoswatIniReader)
        assert isinstance(_ini_reader, KoswatReaderProtocol)
        assert not _ini_reader.koswat_ini_fom_type
