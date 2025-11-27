import os
from pathlib import Path

from koswat.configuration.io.config_sections import (
    AnalysisSectionFom,
    CofferdamReinforcementSectionFom,
    DikeProfileSectionFom,
    InfrastructureSectionFom,
    PipingWallReinforcementSectionFom,
    SoilReinforcementSectionFom,
    StabilitywallReinforcementSectionFom,
    SurroundingsSectionFom,
    VPSReinforcementSectionFom,
)
from koswat.configuration.io.json.koswat_general_json_fom import KoswatGeneralJsonFom
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from tests import test_data

test_json_reader_data = test_data.joinpath("json_reader")


class TestKoswatGeneralJsonFom:
    def test_from_config(self):
        # 1. Define test data.
        _test_file_path = test_json_reader_data.joinpath("koswat_general.json")
        _json_reader = KoswatJsonReader()

        # 2. Run test
        _json = _json_reader.read(_test_file_path)
        _config_fom = KoswatGeneralJsonFom.from_json(_json)

        # 3. Validate expectations.
        assert isinstance(_config_fom, KoswatGeneralJsonFom)

        # Analysis section
        assert isinstance(_config_fom.analysis_section, AnalysisSectionFom)
        # These paths are not included in the test dir so None will be mapped in the FOM.
        assert _config_fom.analysis_section.dike_section_location_shp_file == Path(
            "c:\\fake_drive\\Invoer\\Dijkringlijnen_KOSWAT_2017_WV21_DR10.shp"
        )
        assert _config_fom.analysis_section.dike_selection_txt_file == Path(
            "c:\\fake_drive\\Invoer\\json files\\DijksectieSelectie.txt"
        )
        assert _config_fom.analysis_section.input_profiles_json_dir == Path(
            "c:\\fake_drive\\Invoer\\dike_section_input"
        )
        assert _config_fom.analysis_section.scenarios_json_dir == Path(
            "c:\\fake_drive\\Invoer\\Scenarios"
        )
        # No databaes loaded because the path is not included in the test data.
        assert _config_fom.analysis_section.surroundings_database_dir == Path(
            "c:\\fake_drive\\Invoer\\Omgevingsanalyses"
        )
        assert _config_fom.analysis_section.costs_json_file == Path(
            "c:\\fake_drive\\Invoer\\json files\\Eenheidsprijzen2017.json"
        )
        assert _config_fom.analysis_section.analysis_output_dir == Path(
            "c:\\fake_drive\\Uitvoer"
        )
        assert _config_fom.analysis_section.include_taxes == True

        # Dijkprofiel section
        assert isinstance(_config_fom.dike_profile_section, DikeProfileSectionFom)
        assert _config_fom.dike_profile_section.thickness_grass_layer == 0.3
        assert _config_fom.dike_profile_section.thickness_clay_layer == 0.5

        # Grondmaatregel section
        assert isinstance(_config_fom.soil_measure_section, SoilReinforcementSectionFom)
        assert (
            _config_fom.soil_measure_section.soil_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _config_fom.soil_measure_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert _config_fom.soil_measure_section.min_berm_height == 0.5
        assert _config_fom.soil_measure_section.max_berm_height_factor == 0.4
        assert _config_fom.soil_measure_section.factor_increase_berm_height == 0.05

        # Verticale piping oplossing section
        assert isinstance(_config_fom.vps_section, VPSReinforcementSectionFom)
        assert _config_fom.vps_section.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert (
            _config_fom.vps_section.constructive_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _config_fom.soil_measure_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert _config_fom.vps_section.polderside_berm_width_vps == 10

        # Kwelscherm section
        assert isinstance(
            _config_fom.piping_wall_section, PipingWallReinforcementSectionFom
        )
        assert (
            _config_fom.piping_wall_section.soil_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _config_fom.stability_wall_section.constructive_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _config_fom.piping_wall_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert _config_fom.piping_wall_section.min_length_piping_wall == 4
        assert _config_fom.piping_wall_section.transition_cbwall_sheetpile == 99
        assert _config_fom.piping_wall_section.max_length_piping_wall == 25

        # Stabiliteitswand section
        assert isinstance(
            _config_fom.stability_wall_section, StabilitywallReinforcementSectionFom
        )
        assert (
            _config_fom.stability_wall_section.soil_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert (
            _config_fom.stability_wall_section.constructive_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _config_fom.stability_wall_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert _config_fom.stability_wall_section.steepening_polderside_slope == 2
        assert _config_fom.stability_wall_section.min_length_stability_wall == 5
        assert (
            _config_fom.stability_wall_section.transition_sheetpile_diaphragm_wall == 20
        )
        assert _config_fom.stability_wall_section.max_length_stability_wall == 25

        # Kistdam section
        assert isinstance(
            _config_fom.cofferdam_section, CofferdamReinforcementSectionFom
        )
        assert (
            _config_fom.cofferdam_section.soil_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert (
            _config_fom.cofferdam_section.constructive_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert _config_fom.cofferdam_section.min_length_cofferdam == 5
        assert _config_fom.cofferdam_section.max_length_cofferdam == 25

        # Omgeving section
        assert isinstance(_config_fom.surroundings_section, SurroundingsSectionFom)
        assert _config_fom.surroundings_section.construction_distance == 50
        assert _config_fom.surroundings_section.construction_buffer == 10
        assert _config_fom.surroundings_section.waterside is False
        assert _config_fom.surroundings_section.buildings is True
        assert _config_fom.surroundings_section.railways is False
        assert _config_fom.surroundings_section.waters is False

        # Infrastructuur section
        assert isinstance(_config_fom.infrastructuur_section, InfrastructureSectionFom)
        assert _config_fom.infrastructuur_section.active == False
        assert (
            _config_fom.infrastructuur_section.surtax_factor_roads
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            _config_fom.infrastructuur_section.infrastructure_costs_0dh
            == InfraCostsEnum.GEEN
        )
        assert _config_fom.infrastructuur_section.buffer_waterside == 0
        assert _config_fom.infrastructuur_section.roads_class2_width == 2
        assert _config_fom.infrastructuur_section.roads_class24_width == 5
        assert _config_fom.infrastructuur_section.roads_class47_width == 8
        assert _config_fom.infrastructuur_section.roads_class7_width == 12
        assert _config_fom.infrastructuur_section.roads_unknown_width == 8
