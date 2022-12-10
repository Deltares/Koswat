from typing import Type

import pytest

from koswat.configuration.io.ini.koswat_costs_ini_fom import *
from koswat.configuration.io.ini.koswat_dike_selection_ini_fom import *
from koswat.configuration.io.ini.koswat_general_ini_fom import *
from koswat.configuration.io.ini.koswat_scenario_ini_fom import *
from koswat.io.file_object_model_protocol import ImportFileObjectModelProtocol
from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol
from koswat.io.ini.koswat_ini_reader import KoswatIniReader
from tests import test_data

test_ini_reader_data = test_data / "ini_reader"

class TestReadIniConfigurations:
    @pytest.mark.parametrize(
        "test_file, ini_fom_type",
        [
            pytest.param("koswat_general.ini", KoswatGeneralIniFom, id="General INI"),
            pytest.param("koswat_costs.ini", KoswatCostsIniFom, id="Costs INI"),
            pytest.param(
                "koswat_scenario.ini", KoswatScenarioIniFom, id="Scenario INI"
            ),
            pytest.param(
                "koswat_dike_selection.ini",
                KoswatDikeSelectionIniFom,
                id="Dike sections INI",
            ),
        ],
    )
    def test_koswat_ini_reader_returns_fom_instance(
        self, test_file: str, ini_fom_type: Type[KoswatIniFomProtocol]
    ):
        # 1. Define test data.
        _test_file_path = test_ini_reader_data / test_file
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
        _test_file_path = test_ini_reader_data / "koswat_general.ini"
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

    def test_koswat_ini_read_costs_ini(self):
        # 1. Define test data.
        _test_file_path = test_ini_reader_data / "koswat_costs.ini"
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = KoswatCostsIniFom

        # 2. Run test
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_ini_fom, KoswatCostsIniFom)

        # Eenheidsprijzen
        assert isinstance(_ini_fom.eenheidsprijzen_section, EenheidsprijzenSection)
        assert _ini_fom.eenheidsprijzen_section.prijspeil == 2017

        # KostenDijkProfiel
        assert isinstance(_ini_fom.kostendijkprofiel_section, KostenDijkprofielSection)
        assert _ini_fom.kostendijkprofiel_section.aanleg_graslaag_m3 == 12.44
        assert _ini_fom.kostendijkprofiel_section.aanleg_kleilaag_m3 == 18.05
        assert _ini_fom.kostendijkprofiel_section.aanleg_kern_m3 == 10.98
        assert _ini_fom.kostendijkprofiel_section.hergebruik_graslaag_m3 == 6.04
        assert _ini_fom.kostendijkprofiel_section.hergebruik_kern_m3 == 4.67
        assert _ini_fom.kostendijkprofiel_section.afvoeren_materiaal_m3 == 7.07
        assert _ini_fom.kostendijkprofiel_section.profileren_graslaag_m2 == 0.88
        assert _ini_fom.kostendijkprofiel_section.profileren_kleilaag_m2 == 0.65
        assert _ini_fom.kostendijkprofiel_section.profileren_kern_m2 == 0.60
        assert _ini_fom.kostendijkprofiel_section.bewerken_maaiveld_m2 == 0.25

        # KostenInfrastructuur
        assert isinstance(
            _ini_fom.kosteninfrastructuur_section, KostenInfrastructuurSection
        )
        assert _ini_fom.kosteninfrastructuur_section.wegen_klasse2_verwijderen == 7.40
        assert _ini_fom.kosteninfrastructuur_section.wegen_klasse24_verwijderen == 9.64
        assert _ini_fom.kosteninfrastructuur_section.wegen_klasse47_verwijderen == 23.99
        assert _ini_fom.kosteninfrastructuur_section.wegen_klasse7_verwijderen == 38.77
        assert _ini_fom.kosteninfrastructuur_section.wegen_onbekend_verwijderen == 9.64
        assert _ini_fom.kosteninfrastructuur_section.wegen_klasse2_aanleg == 24.31
        assert _ini_fom.kosteninfrastructuur_section.wegen_klasse24_aanleg == 32.30
        assert _ini_fom.kosteninfrastructuur_section.wegen_klasse47_aanleg == 31.85
        assert _ini_fom.kosteninfrastructuur_section.wegen_klasse7_aanleg == 36.64
        assert _ini_fom.kosteninfrastructuur_section.wegen_onbekend_aanleg == 32.30

        # KostenOpslagFactorenInclBTW
        assert isinstance(
            _ini_fom.kostenopslagfactoreninclbtw_section,
            KostenOpslagfactorenInclBTWSection,
        )
        assert _ini_fom.kostenopslagfactoreninclbtw_section.grond_makkelijk == 1.714
        assert _ini_fom.kostenopslagfactoreninclbtw_section.grond_normaal == 1.953
        assert _ini_fom.kostenopslagfactoreninclbtw_section.grond_moeilijk == 2.177
        assert (
            _ini_fom.kostenopslagfactoreninclbtw_section.constructief_makkelijk == 2.097
        )
        assert (
            _ini_fom.kostenopslagfactoreninclbtw_section.constructief_normaal == 2.413
        )
        assert (
            _ini_fom.kostenopslagfactoreninclbtw_section.constructief_moeilijk == 2.690
        )
        assert _ini_fom.kostenopslagfactoreninclbtw_section.wegen_makkelijk == 2.097
        assert _ini_fom.kostenopslagfactoreninclbtw_section.wegen_normaal == 2.413
        assert _ini_fom.kostenopslagfactoreninclbtw_section.wegen_moeilijk == 2.690
        assert (
            _ini_fom.kostenopslagfactoreninclbtw_section.grondaankoop_makkelijk == 1.292
        )
        assert (
            _ini_fom.kostenopslagfactoreninclbtw_section.grondaankoop_normaal == 1.412
        )
        assert (
            _ini_fom.kostenopslagfactoreninclbtw_section.grondaankoop_moeilijk == 1.645
        )

        # KostenOpslagFactorenexclBTW
        assert isinstance(
            _ini_fom.kostenopslagfactorenexclbtw_section,
            KostenOpslagfactorenExclBTWSection,
        )
        assert _ini_fom.kostenopslagfactorenexclbtw_section.grond_makkelijk == 1.421
        assert _ini_fom.kostenopslagfactorenexclbtw_section.grond_normaal == 1.621
        assert _ini_fom.kostenopslagfactorenexclbtw_section.grond_moeilijk == 1.810
        assert (
            _ini_fom.kostenopslagfactorenexclbtw_section.constructief_makkelijk == 1.741
        )
        assert (
            _ini_fom.kostenopslagfactorenexclbtw_section.constructief_normaal == 2.003
        )
        assert (
            _ini_fom.kostenopslagfactorenexclbtw_section.constructief_moeilijk == 2.233
        )
        assert _ini_fom.kostenopslagfactorenexclbtw_section.wegen_makkelijk == 1.741
        assert _ini_fom.kostenopslagfactorenexclbtw_section.wegen_normaal == 2.003
        assert _ini_fom.kostenopslagfactorenexclbtw_section.wegen_moeilijk == 2.233
        assert (
            _ini_fom.kostenopslagfactorenexclbtw_section.grondaankoop_makkelijk == 1.292
        )
        assert (
            _ini_fom.kostenopslagfactorenexclbtw_section.grondaankoop_normaal == 1.412
        )
        assert (
            _ini_fom.kostenopslagfactorenexclbtw_section.grondaankoop_moeilijk == 1.645
        )

    def test_koswat_ini_read_dike_selection_ini(self):
        # 1. Define test data.
        _test_file_path = test_ini_reader_data / "koswat_dike_selection.ini"
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = KoswatDikeSelectionIniFom

        # 2. Run test
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_ini_fom, KoswatDikeSelectionIniFom)

        # Dijksecties
        assert len(_ini_fom.dijksecties_section.dike_sections) == 3
        assert _ini_fom.dijksecties_section.dike_sections[0] == "10-1-1-A-1-A"
        assert _ini_fom.dijksecties_section.dike_sections[1] == "10-1-2-A-1-A"
        assert _ini_fom.dijksecties_section.dike_sections[2] == "10-1-3-A-1-B-1"

    def test_koswat_ini_read_scenario_ini(self):
        # 1. Define test data.
        _test_file_path = test_ini_reader_data / "koswat_scenario.ini"
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = KoswatScenarioIniFom

        # 2. Run test
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_ini_fom, KoswatScenarioIniFom)

        # Scenarios
        assert len(_ini_fom.scenario_sections) == 2

        # Scenario 0
        assert _ini_fom.scenario_sections[0].dH == 0.5
        assert _ini_fom.scenario_sections[0].dS == 10
        assert _ini_fom.scenario_sections[0].dP == 50
        assert _ini_fom.scenario_sections[0].buitentalud == None
        assert _ini_fom.scenario_sections[0].kruinbreedte == None

        # Scenario 1
        assert _ini_fom.scenario_sections[1].dH == 1
        assert _ini_fom.scenario_sections[1].dS == 15
        assert _ini_fom.scenario_sections[1].dP == 75
        assert _ini_fom.scenario_sections[1].buitentalud == 4
        assert _ini_fom.scenario_sections[1].kruinbreedte == 10
