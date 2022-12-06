import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.io.ini import KoswatIniCofferDamFom
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class TestKoswatIniCofferDamFom:
    def test_initialize_koswat_ini_coffer_dam_fom(self):
        _ini_coffer_dam_fom = KoswatIniCofferDamFom()
        assert isinstance(_ini_coffer_dam_fom, KoswatIniCofferDamFom)
        assert isinstance(_ini_coffer_dam_fom, FileObjectModelProtocol)
        assert _ini_coffer_dam_fom.storageFactorGround == ""
        assert not _ini_coffer_dam_fom.is_valid()
