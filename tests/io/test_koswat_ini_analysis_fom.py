import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.io.ini.koswat_ini_analysis_fom import (
    KoswatIniAnalysisFom,  # , KoswatIniAnalysisFomBuilder
)
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class TestKoswatIniAnalysisFom:
    def test_initialize_koswat_ini_analysis_fom(self):
        _ini_analysis_fom = KoswatIniAnalysisFom()
        assert isinstance(_ini_analysis_fom, KoswatIniAnalysisFom)
        assert isinstance(_ini_analysis_fom, FileObjectModelProtocol)
        assert _ini_analysis_fom.dijksectiesSelectie == ""
        assert not _ini_analysis_fom.is_valid()
