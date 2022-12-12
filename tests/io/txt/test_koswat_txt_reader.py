from koswat.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.io.txt.koswat_txt_reader import KoswatTxtReader


class TestKoswatTxtReader:
    def test_koswat_txt_reader_init(self):
        _txt_reader = KoswatTxtReader()
        assert isinstance(_txt_reader, KoswatTxtReader)
        assert isinstance(_txt_reader, KoswatReaderProtocol)
        assert not _txt_reader.koswat_txt_fom_type
