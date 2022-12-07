import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.io.ini import KoswatIniCofferDamFom, KoswatIniCofferDamFomBuilder
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class TestKoswatIniCofferDamFom:
    def test_initialize_koswat_ini_coffer_dam_fom(self):
        _ini_coffer_dam_fom = KoswatIniCofferDamFom()
        assert isinstance(_ini_coffer_dam_fom, KoswatIniCofferDamFom)
        assert isinstance(_ini_coffer_dam_fom, FileObjectModelProtocol)
        assert _ini_coffer_dam_fom.storageFactorGround == ""
        assert not _ini_coffer_dam_fom.is_valid()


class TestKoswatIniCofferDamFomBuilder:
    def test_initialize_empty_koswat_ini_coffer_dam_fom_builder(self):
        fom_builder = KoswatIniCofferDamFomBuilder()
        assert isinstance(fom_builder, KoswatIniCofferDamFomBuilder) == True
        assert isinstance(fom_builder, BuilderProtocol) == True
        assert not fom_builder.section
        assert not fom_builder._is_valid()

    def test_initialize_with_dict_koswat_ini_coffer_dam_fom_builder(self):
        fom_builder = KoswatIniCofferDamFomBuilder()
        fom_builder.section = dict(
            {
                "Opslagfactor_Grond": "Opslagfactor_Grond1",
                "Opslagfactor_Constructief": "Opslagfactor_Constructief1",
                "Min_Lengte_Kistdam": "14",
                "Max_Lengte_Kistdam": "21",
            }
        )
        fom = fom_builder.build()
        assert fom.storageFactorGround == "Opslagfactor_Grond1"
        assert fom.storageFactorConstruction == "Opslagfactor_Constructief1"
        assert fom.minLenghtCofferDam == 14
        assert fom.maxLenghtCofferDam == 21
        assert fom.is_valid()


# TODO fix test. Test on uninitialized in is_valid() fails on float type
# def test_initialize_with_half_dict_koswat_ini_coffer_dam_fom_builder(self):
#     fom_builder = KoswatIniCofferDamFomBuilder()
#     fom_builder.section = dict(
#         {
#             "Opslagfactor_Grond": "Opslagfactor_Grond1",
#             "Min_Lengte_Kistdam": "14",
#         }
#     )
#     fom = fom_builder.build()
#     assert not fom.is_valid()
