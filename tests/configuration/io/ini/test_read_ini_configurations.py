from pathlib import Path
from typing import Type

import pytest

from koswat.configuration.io.ini.koswat_costs_ini_fom import (
    ConstructionCostsSectionFom,
    DikeProfileCostsSectionFom,
    InfrastructureCostsSectionFom,
    KoswatCostsIniFom,
    SurtaxCostsSectionFom,
    UnitPricesSectionFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import (
    AnalysisSectionFom,
    CofferdamReinforcementSectionFom,
    DikeProfileSectionFom,
    InfrastructureSectionFom,
    KoswatGeneralIniFom,
    PipingWallReinforcementSectionFom,
    SoilReinforcementSectionFom,
    StabilitywallReinforcementSectionFom,
    SurroundingsSectionFom,
    VPSReinforcementSectionFom,
)
from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
)
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol
from koswat.core.io.ini.koswat_ini_reader import KoswatIniReader
from tests import test_data

test_ini_reader_data = test_data.joinpath("ini_reader")


class TestReadIniConfigurations:
    @pytest.mark.parametrize(
        "test_file, ini_fom_type",
        [
            pytest.param("koswat_general.ini", KoswatGeneralIniFom, id="General INI"),
            pytest.param("koswat_costs.ini", KoswatCostsIniFom, id="Costs INI"),
            pytest.param(
                "koswat_scenario.ini", KoswatSectionScenariosIniFom, id="Scenario INI"
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
        assert isinstance(_ini_fom, FileObjectModelProtocol)

    def test_koswat_ini_read_general_ini(self):
        # 1. Define test data.
        _test_file_path = test_ini_reader_data.joinpath("koswat_general.ini")
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = KoswatGeneralIniFom

        # 2. Run test
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_ini_fom, KoswatGeneralIniFom)

        # Analysis section
        assert isinstance(_ini_fom.analysis_section, AnalysisSectionFom)
        # These paths are not included in the test dir so None will be mapped in the FOM.
        assert _ini_fom.analysis_section.dike_selection_txt_file == Path(
            "c:\\fake_drive\\Invoer\\ini files\\DijksectieSelectie.txt"
        )
        assert _ini_fom.analysis_section.dike_section_location_shp_file == Path(
            "c:\\fake_drive\\Invoer\\Dijkringlijnen_KOSWAT_2017_WV21_DR10.shp"
        )
        assert _ini_fom.analysis_section.input_profiles_json_dir == Path(
            "c:\\fake_drive\\Invoer\\json\\dikesection_input"
        )
        assert _ini_fom.analysis_section.scenarios_ini_dir == Path(
            "c:\\fake_drive\\Invoer\\Scenarios"
        )
        assert _ini_fom.analysis_section.costs_ini_file == Path(
            "c:\\fake_drive\\Invoer\\ini files\\Eenheidsprijzen2017.ini"
        )
        assert _ini_fom.analysis_section.analysis_output_dir == Path(
            "c:\\fake_drive\\Uitvoer"
        )
        assert _ini_fom.analysis_section.include_taxes == True

        # Dijkprofiel section
        assert isinstance(_ini_fom.dike_profile_section, DikeProfileSectionFom)
        assert _ini_fom.dike_profile_section.thickness_grass_layer == 0.3
        assert _ini_fom.dike_profile_section.thickness_clay_layer == 0.5

        # Grondmaatregel section
        assert isinstance(_ini_fom.soil_measure_section, SoilReinforcementSectionFom)
        assert (
            _ini_fom.soil_measure_section.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.soil_measure_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert _ini_fom.soil_measure_section.min_berm_height == 0.5
        assert _ini_fom.soil_measure_section.max_berm_height_factor == 0.4
        assert _ini_fom.soil_measure_section.factor_increase_berm_height == 0.05

        # Verticale piping oplossing section
        assert isinstance(_ini_fom.vps_section, VPSReinforcementSectionFom)
        assert _ini_fom.vps_section.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert (
            _ini_fom.vps_section.constructive_surtax_factor == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.soil_measure_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert _ini_fom.vps_section.polderside_berm_width_vps == 10

        # Kwelscherm section
        assert isinstance(
            _ini_fom.piping_wall_section, PipingWallReinforcementSectionFom
        )
        assert (
            _ini_fom.piping_wall_section.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.stability_wall_section.constructive_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.piping_wall_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert _ini_fom.piping_wall_section.min_length_piping_wall == 4
        assert _ini_fom.piping_wall_section.transition_cbwall_sheetpile == 99
        assert _ini_fom.piping_wall_section.max_length_piping_wall == 25

        # Stabiliteitswand section
        assert isinstance(
            _ini_fom.stability_wall_section, StabilitywallReinforcementSectionFom
        )
        assert (
            _ini_fom.stability_wall_section.soil_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert (
            _ini_fom.stability_wall_section.constructive_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.stability_wall_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert _ini_fom.stability_wall_section.steepening_polderside_slope == 2
        assert _ini_fom.stability_wall_section.min_length_stability_wall == 5
        assert _ini_fom.stability_wall_section.transition_sheetpile_diaphragm_wall == 20
        assert _ini_fom.stability_wall_section.max_length_stability_wall == 25

        # Kistdam section
        assert isinstance(_ini_fom.cofferdam_section, CofferdamReinforcementSectionFom)
        assert (
            _ini_fom.cofferdam_section.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        )
        assert (
            _ini_fom.cofferdam_section.constructive_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert _ini_fom.cofferdam_section.min_length_cofferdam == 5
        assert _ini_fom.cofferdam_section.max_length_cofferdam == 25

        # Omgeving section
        assert isinstance(_ini_fom.surroundings_section, SurroundingsSectionFom)
        # No databaes loaded because the path is not included in the test data.
        assert _ini_fom.surroundings_section.surroundings_database_dir == Path(
            "c:\\fake_drive\\Invoer\\Omgevingsanalyses"
        )
        assert _ini_fom.surroundings_section.construction_distance == 50
        assert _ini_fom.surroundings_section.construction_buffer == 10
        assert _ini_fom.surroundings_section.waterside is False
        assert _ini_fom.surroundings_section.buildings is True
        assert _ini_fom.surroundings_section.railways is False
        assert _ini_fom.surroundings_section.waters is False

        # Infrastructuur section
        assert isinstance(_ini_fom.infrastructuur_section, InfrastructureSectionFom)
        assert _ini_fom.infrastructuur_section.infrastructure == False
        assert (
            _ini_fom.infrastructuur_section.surtax_factor_roads
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _ini_fom.infrastructuur_section.infrastructure_costs_0dh
            == InfraCostsEnum.GEEN
        )
        assert _ini_fom.infrastructuur_section.buffer_waterside == 0
        assert _ini_fom.infrastructuur_section.roads_class2_width == 2
        assert _ini_fom.infrastructuur_section.roads_class24_width == 5
        assert _ini_fom.infrastructuur_section.roads_class47_width == 8
        assert _ini_fom.infrastructuur_section.roads_class7_width == 12
        assert _ini_fom.infrastructuur_section.roads_unknown_width == 8

    def test_koswat_ini_read_scenario_ini(self):
        # 1. Define test data.
        _test_file_path = test_ini_reader_data / "koswat_scenario.ini"
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = KoswatSectionScenariosIniFom

        # 2. Run test
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_ini_fom, KoswatSectionScenariosIniFom)

        # Scenarios
        assert len(_ini_fom.section_scenarios) == 2

        # Scenario 0
        assert _ini_fom.section_scenarios[0].d_h == 0.5
        assert _ini_fom.section_scenarios[0].d_s == 10
        assert _ini_fom.section_scenarios[0].d_p == 50
        assert _ini_fom.section_scenarios[0].waterside_slope == None
        assert _ini_fom.section_scenarios[0].crest_width == None

        # Scenario 1
        assert _ini_fom.section_scenarios[1].d_h == 1
        assert _ini_fom.section_scenarios[1].d_s == 15
        assert _ini_fom.section_scenarios[1].d_p == 75
        assert _ini_fom.section_scenarios[1].waterside_slope == 4
        assert _ini_fom.section_scenarios[1].crest_width == 10
