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
    PipingwallReinforcementSectionFom,
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

test_ini_reader_data = test_data / "ini_reader"


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
        _test_file_path = test_ini_reader_data / "koswat_general.ini"
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
        assert _ini_fom.analysis_section.input_profiles_csv_file == Path(
            "c:\\fake_drive\\Invoer\\InputPerDijkvak_WV21_KOSWAT_v2022_DR10.csv"
        )
        assert _ini_fom.analysis_section.scenarios_ini_file == Path(
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
            _ini_fom.piping_wall_section, PipingwallReinforcementSectionFom
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
        assert _ini_fom.piping_wall_section.transition_cbwall_sheet_pile == 99
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
        assert (
            _ini_fom.stability_wall_section.transition_sheet_pile_diaphragm_wall == 20
        )
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
        assert _ini_fom.surroundings_section.waterside == False
        assert _ini_fom.surroundings_section.buildings == True
        assert _ini_fom.surroundings_section.railways == False
        assert _ini_fom.surroundings_section.waters == False

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

        # 1. Define test data.
        _test_file_path = test_ini_reader_data / "koswat_costs.ini"
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = KoswatCostsIniFom

        # 2. Run test
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_ini_fom, KoswatCostsIniFom)

        # Eenheidsprijzen
        assert isinstance(_ini_fom.unit_prices_section, UnitPricesSectionFom)
        assert _ini_fom.unit_prices_section.price_level == 2017

        # KostenDijkProfiel
        assert isinstance(
            _ini_fom.dike_profile_costs_section, DikeProfileCostsSectionFom
        )
        assert _ini_fom.dike_profile_costs_section.construction_grass_layer_m3 == 12.44
        assert _ini_fom.dike_profile_costs_section.construction_clay_layer_m3 == 18.05
        assert _ini_fom.dike_profile_costs_section.construction_sand_m3 == 10.98
        assert _ini_fom.dike_profile_costs_section.reuse_grass_layer_m3 == 6.04
        assert _ini_fom.dike_profile_costs_section.reuse_sand_m3 == 4.67
        assert _ini_fom.dike_profile_costs_section.dispose_material_m3 == 7.07
        assert _ini_fom.dike_profile_costs_section.profile_grass_layer_m2 == 0.88
        assert _ini_fom.dike_profile_costs_section.profile_clay_layer_m2 == 0.65
        assert _ini_fom.dike_profile_costs_section.profile_sand_m2 == 0.60
        assert (
            _ini_fom.dike_profile_costs_section.process_ground_level_surface_m2 == 0.25
        )

        # KostenInfrastructuur
        assert isinstance(
            _ini_fom.infrastructure_costs_section, InfrastructureCostsSectionFom
        )
        assert _ini_fom.infrastructure_costs_section.roads_class2_removal == 7.40
        assert _ini_fom.infrastructure_costs_section.roads_class24_removal == 9.64
        assert _ini_fom.infrastructure_costs_section.roads_class47_removal == 23.99
        assert _ini_fom.infrastructure_costs_section.roads_class7_removal == 38.77
        assert _ini_fom.infrastructure_costs_section.roads_unknown_removal == 9.64
        assert _ini_fom.infrastructure_costs_section.roads_class2_construction == 24.31
        assert _ini_fom.infrastructure_costs_section.roads_class24_construction == 32.30
        assert _ini_fom.infrastructure_costs_section.roads_class47_construction == 31.85
        assert _ini_fom.infrastructure_costs_section.roads_class7_construction == 36.64
        assert _ini_fom.infrastructure_costs_section.roads_unknown_construction == 32.30

        # KostenOpslagFactorenInclBTW
        assert isinstance(
            _ini_fom.surtax_costs_incl_tax_section,
            SurtaxCostsSectionFom,
        )
        assert _ini_fom.surtax_costs_incl_tax_section.soil_easy == 1.714
        assert _ini_fom.surtax_costs_incl_tax_section.soil_normal == 1.953
        assert _ini_fom.surtax_costs_incl_tax_section.soil_hard == 2.177
        assert _ini_fom.surtax_costs_incl_tax_section.constructive_easy == 2.097
        assert _ini_fom.surtax_costs_incl_tax_section.constructive_normal == 2.413
        assert _ini_fom.surtax_costs_incl_tax_section.constructive_hard == 2.690
        assert _ini_fom.surtax_costs_incl_tax_section.road_easy == 2.097
        assert _ini_fom.surtax_costs_incl_tax_section.roads_normal == 2.413
        assert _ini_fom.surtax_costs_incl_tax_section.roads_hard == 2.690
        assert _ini_fom.surtax_costs_incl_tax_section.land_purchase_easy == 1.292
        assert _ini_fom.surtax_costs_incl_tax_section.land_purchase_normal == 1.412
        assert _ini_fom.surtax_costs_incl_tax_section.land_purchase_hard == 1.645

        # KostenOpslagFactorenExclBTW
        assert isinstance(
            _ini_fom.surtax_costs_excl_tax_section,
            SurtaxCostsSectionFom,
        )
        assert _ini_fom.surtax_costs_excl_tax_section.soil_easy == 1.421
        assert _ini_fom.surtax_costs_excl_tax_section.soil_normal == 1.621
        assert _ini_fom.surtax_costs_excl_tax_section.soil_hard == 1.810
        assert _ini_fom.surtax_costs_excl_tax_section.constructive_easy == 1.741
        assert _ini_fom.surtax_costs_excl_tax_section.constructive_normal == 2.003
        assert _ini_fom.surtax_costs_excl_tax_section.constructive_hard == 2.233
        assert _ini_fom.surtax_costs_excl_tax_section.road_easy == 1.741
        assert _ini_fom.surtax_costs_excl_tax_section.roads_normal == 2.003
        assert _ini_fom.surtax_costs_excl_tax_section.roads_hard == 2.233
        assert _ini_fom.surtax_costs_excl_tax_section.land_purchase_easy == 1.292
        assert _ini_fom.surtax_costs_excl_tax_section.land_purchase_normal == 1.412
        assert _ini_fom.surtax_costs_excl_tax_section.land_purchase_hard == 1.645

        # KostenCBwand
        assert isinstance(
            _ini_fom.construction_cost_cb_wall,
            ConstructionCostsSectionFom,
        )
        assert _ini_fom.construction_cost_cb_wall.c_factor == 0
        assert _ini_fom.construction_cost_cb_wall.d_factor == 159.326
        assert _ini_fom.construction_cost_cb_wall.z_factor == -34.794
        assert _ini_fom.construction_cost_cb_wall.f_factor == 0
        assert _ini_fom.construction_cost_cb_wall.g_factor == 0

        # KostenDamwandOnverankerd
        assert isinstance(
            _ini_fom.construction_cost_sheet_pile_unanchored,
            ConstructionCostsSectionFom,
        )
        assert _ini_fom.construction_cost_sheet_pile_unanchored.c_factor == 9.298
        assert _ini_fom.construction_cost_sheet_pile_unanchored.d_factor == 132.239
        assert _ini_fom.construction_cost_sheet_pile_unanchored.z_factor == 103.628
        assert _ini_fom.construction_cost_sheet_pile_unanchored.f_factor == 0
        assert _ini_fom.construction_cost_sheet_pile_unanchored.g_factor == 0

        # KostenDamwandVerankerd
        assert isinstance(
            _ini_fom.construction_cost_sheet_pile_anchored,
            ConstructionCostsSectionFom,
        )
        assert _ini_fom.construction_cost_sheet_pile_anchored.c_factor == 9.298
        assert _ini_fom.construction_cost_sheet_pile_anchored.d_factor == 150.449
        assert _ini_fom.construction_cost_sheet_pile_anchored.z_factor == 1304.455
        assert _ini_fom.construction_cost_sheet_pile_anchored.f_factor == 0
        assert _ini_fom.construction_cost_sheet_pile_anchored.g_factor == 0

        # KostenDiepwand
        assert isinstance(
            _ini_fom.construction_cost_diaphragm_wall,
            ConstructionCostsSectionFom,
        )
        assert _ini_fom.construction_cost_diaphragm_wall.c_factor == 0
        assert _ini_fom.construction_cost_diaphragm_wall.d_factor == 0
        assert _ini_fom.construction_cost_diaphragm_wall.z_factor == 0
        assert _ini_fom.construction_cost_diaphragm_wall.f_factor == 281.176
        assert _ini_fom.construction_cost_diaphragm_wall.g_factor == 1.205

        # KostenKistdam
        assert isinstance(
            _ini_fom.construction_cost_cofferdam,
            ConstructionCostsSectionFom,
        )
        assert _ini_fom.construction_cost_cofferdam.c_factor == 0
        assert _ini_fom.construction_cost_cofferdam.d_factor == 680.782
        assert _ini_fom.construction_cost_cofferdam.z_factor == -74.602
        assert _ini_fom.construction_cost_cofferdam.f_factor == 0
        assert _ini_fom.construction_cost_cofferdam.g_factor == 0

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
        assert _ini_fom.section_scenarios[0].buiten_talud == None
        assert _ini_fom.section_scenarios[0].kruin_breedte == None

        # Scenario 1
        assert _ini_fom.section_scenarios[1].d_h == 1
        assert _ini_fom.section_scenarios[1].d_s == 15
        assert _ini_fom.section_scenarios[1].d_p == 75
        assert _ini_fom.section_scenarios[1].buiten_talud == 4
        assert _ini_fom.section_scenarios[1].kruin_breedte == 10
