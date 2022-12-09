from typing import Type

import pytest

from koswat.io.file_object_model_protocol import ImportFileObjectModelProtocol
from koswat.io.ini.koswat_general_ini_fom import *
from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol
from koswat.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.io.koswat_reader_protocol import KoswatReaderProtocol
from tests import test_data


class TestKoswatIniReader:
    def test_koswat_ini_reader_init(self):
        _ini_reader = KoswatIniReader()
        assert isinstance(_ini_reader, KoswatIniReader)
        assert isinstance(_ini_reader, KoswatReaderProtocol)
        assert not _ini_reader.koswat_ini_fom_type

    @pytest.mark.parametrize(
        "test_file, ini_fom_type",
        [pytest.param("koswat_general.ini", KoswatGeneralIniFom, id="General INI")],
    )
    def test_koswat_ini_reader_returns_fom_instance(
        self, test_file: str, ini_fom_type: Type[KoswatIniFomProtocol]
    ):
        # 1. Define test data.
        _test_file_path = test_data / "ini_reader" / test_file
        assert _test_file_path, "Test file not found at {}".format(_test_file_path)
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = ini_fom_type

        # 2. Run test.
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Verify expectations.
        assert isinstance(_ini_fom, ini_fom_type)
        assert isinstance(_ini_fom, ImportFileObjectModelProtocol)

    def test_koswat_ini_read_general_ini(self):
        # 1. Define test data.
        _test_file_path = test_data / "ini_reader" / "koswat_general.ini"
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = KoswatGeneralIniFom

        # 2. Run test
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_ini_fom, KoswatGeneralIniFom)

        # Analysis section
        assert isinstance(_ini_fom.analyse_section, AnalysisSection)
        assert _ini_fom.analyse_section.dijksecties_selectie == Path(
            "p:\\frm-koswat\\KOSWAT v2022\\Invoer\\ini files\\DijksectieSelectie.ini"
        )
        assert _ini_fom.analyse_section.dijksectie_ligging == Path(
            "p:\\frm-koswat\\KOSWAT v2022\\Invoer\\Dijkringlijnen_KOSWAT_2017_WV21_DR10.shp"
        )
        assert _ini_fom.analyse_section.dijksectie_invoer == Path(
            "p:\\frm-koswat\\KOSWAT v2022\\Invoer\\InputPerDijkvak_WV21_KOSWAT_v2022_DR10.csv"
        )
        assert _ini_fom.analyse_section.scenario_invoer == Path(
            "p:\\frm-koswat\\KOSWAT v2022\\Invoer\\Scenarios"
        )
        assert _ini_fom.analyse_section.eenheidsprijzen == Path(
            "p:\\frm-koswat\\KOSWAT v2022\\Invoer\\ini files\\Eenheidsprijzen2017.ini"
        )
        assert _ini_fom.analyse_section.uitvoerfolder == Path(
            "p:\\frm-koswat\\KOSWAT v2022\\Uitvoer"
        )
        assert _ini_fom.analyse_section.btw == True

        # Dijkprofiel section
        assert isinstance(_ini_fom.dijkprofiel_section, DikeProfileSection)
        assert _ini_fom.dijkprofiel_section.dikte_graslaag == 0.3
        assert _ini_fom.dijkprofiel_section.dikte_kleilaag == 0.5

        # Grondmaatregel section
        assert isinstance(_ini_fom.grondmaatregel_section, GrondmaatregelSection)
        assert (
            _ini_fom.grondmaatregel_section.opslagfactor_grond
            == StorageFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.grondmaatregel_section.opslagfactor_constructief
            == StorageFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.grondmaatregel_section.opslagfactor_grondaankoop
            == StorageFactorEnum.NORMAAL
        )
        assert _ini_fom.grondmaatregel_section.min_bermhoogte == 0.5
        assert _ini_fom.grondmaatregel_section.max_bermhoogte_factor == 0.4
        assert _ini_fom.grondmaatregel_section.factor_toename_bermhoogte == 0.05

        assert isinstance(_ini_fom.kwelscherm_section, KwelschermSection)
        assert (
            _ini_fom.kwelscherm_section.opslagfactor_grond == StorageFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.kwelscherm_section.opslagfactor_constructief
            == StorageFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.kwelscherm_section.opslagfactor_grondaankoop
            == StorageFactorEnum.NORMAAL
        )
        assert _ini_fom.kwelscherm_section.min_lengte_kwelscherm == 4
        assert _ini_fom.kwelscherm_section.overgang_cbwand_damwand == 99
        assert _ini_fom.kwelscherm_section.max_lengte_kwelscherm == 25

        # Stabiliteitswand section
        assert isinstance(_ini_fom.stabiliteitswand_section, StabiliteitswandSection)
        assert (
            _ini_fom.stabiliteitswand_section.opslagfactor_grond
            == StorageFactorEnum.MOEILIJK
        )
        assert (
            _ini_fom.stabiliteitswand_section.opslagfactor_constructief
            == StorageFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.stabiliteitswand_section.opslagfactor_grondaankoop
            == StorageFactorEnum.MOEILIJK
        )
        assert _ini_fom.stabiliteitswand_section.versteiling_binnentalud == 2
        assert _ini_fom.stabiliteitswand_section.min_lengte_stabiliteitswand == 5
        assert _ini_fom.stabiliteitswand_section.overgang_damwand_diepwand == 20
        assert _ini_fom.stabiliteitswand_section.max_lengte_stabiliteitswand == 25

        # Kistdam section
        assert isinstance(_ini_fom.kistdam_section, KistdamSection)
        assert _ini_fom.kistdam_section.opslagfactor_grond == StorageFactorEnum.MOEILIJK
        assert (
            _ini_fom.kistdam_section.opslagfactor_constructief
            == StorageFactorEnum.MOEILIJK
        )
        assert (
            _ini_fom.kistdam_section.opslagfactor_grondaankoop
            == StorageFactorEnum.NORMAAL
        )
        assert _ini_fom.kistdam_section.min_lengte_kistdam == 5
        assert _ini_fom.kistdam_section.max_lengte_kistdam == 25

        # Omgeving section
        assert isinstance(_ini_fom.omgeving_section, OmgevingSection)
        assert _ini_fom.omgeving_section.omgevingsdatabases == Path(
            "p:\\frm-koswat\\KOSWAT v2022\\Invoer\\Omgevingsanalyses"
        )
        assert _ini_fom.omgeving_section.constructieafstand == 50
        assert _ini_fom.omgeving_section.constructieovergang == 10
        assert _ini_fom.omgeving_section.buitendijks == False
        assert _ini_fom.omgeving_section.bebouwing == True
        assert _ini_fom.omgeving_section.spoorwegen == False
        assert _ini_fom.omgeving_section.water == False

        # Infrastructuur section
        assert isinstance(_ini_fom.infrastructuur_section, InfrastructuurSection)
        assert _ini_fom.infrastructuur_section.infrastructuur == False
        assert (
            _ini_fom.infrastructuur_section.opslagfactor_wegen
            == StorageFactorEnum.NORMAAL
        )
        assert _ini_fom.infrastructuur_section.infrakosten_0dh == InfraCostsEnum.GEEN
        assert _ini_fom.infrastructuur_section.buffer_buitendijks == 0
        assert _ini_fom.infrastructuur_section.wegen_klasse2_breedte == 2
        assert _ini_fom.infrastructuur_section.wegen_klasse24_breedte == 5
        assert _ini_fom.infrastructuur_section.wegen_klasse47_breedte == 8
        assert _ini_fom.infrastructuur_section.wegen_klasse7_breedte == 12
        assert _ini_fom.infrastructuur_section.wegen_onbekend_breedte == 8
