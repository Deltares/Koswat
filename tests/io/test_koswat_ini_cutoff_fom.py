import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.io.ini import KoswatIniCutoffFom
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class TestKoswatIniCutoffFom:
    def test_initialize_koswat_ini_cutoff_fom(self):
        _ini_cutoff_fom = KoswatIniCutoffFom()
        assert isinstance(_ini_cutoff_fom, KoswatIniCutoffFom)
        assert isinstance(_ini_cutoff_fom, FileObjectModelProtocol)
        assert _ini_cutoff_fom.storageFactorGround == ""
        assert not _ini_cutoff_fom.is_valid()
