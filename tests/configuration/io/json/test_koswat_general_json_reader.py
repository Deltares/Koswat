from pathlib import Path

import pytest

from koswat.configuration.io.config_sections import (
    AnalysisSectionFom,
    CofferdamReinforcementSectionFom,
    DikeProfileSectionFom,
    InfrastructureSectionFom,
    PipingWallReinforcementSectionFom,
    SoilReinforcementSectionFom,
    SoilWatersideReinforcementSectionFom,
    StabilityWallCrestReinforcementSectionFom,
    StabilityWallToeReinforcementSectionFom,
    SurroundingsSectionFom,
    VPSReinforcementSectionFom,
)
from koswat.configuration.io.json.koswat_general_json_fom import KoswatGeneralJsonFom
from koswat.configuration.io.json.koswat_general_json_reader import (
    KoswatGeneralJsonReader,
)
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from tests import test_data

test_json_reader_data = test_data.joinpath("json_reader")


class TestKoswatGeneralJsonReader:

    @pytest.mark.parametrize("ground_price_waterside", [None, float("nan")])
    def test_when__normalize_imported_json_given_allow_waterside_reinforcement_and_no_ground_price_then_sets_ground_price_to_zero(
        self,
        ground_price_waterside,
    ):
        class MockedSurroundingsSectionFom(SurroundingsSectionFom):
            def __init__(self):
                self.allow_waterside_reinforcement = False

        class MockedDikeProfileSectionFom(DikeProfileSectionFom):
            def __init__(self):
                self.ground_price_waterside = ground_price_waterside

        class MockedKoswatGeneralJsonFom(KoswatGeneralJsonFom):
            def __init__(self):
                self.surroundings_section = MockedSurroundingsSectionFom()
                self.dike_profile_section = MockedDikeProfileSectionFom()

        # 1. Define test data.
        _json_reader = KoswatGeneralJsonReader()
        _generated_object = MockedKoswatGeneralJsonFom()

        # 2. Run test
        _config_fom = _json_reader._normalize_imported_json(_generated_object)

        # 3. Validate expectations.
        assert _config_fom.dike_profile_section.ground_price_waterside == 0

    def test_when_read_given_valid_json_then_returns_config_fom(self):
        # 1. Define test data.
        _test_file_path = test_json_reader_data.joinpath("koswat_general.json")
        _json_reader = KoswatGeneralJsonReader()

        # 2. Run test
        _config_fom = _json_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_config_fom, KoswatGeneralJsonFom)
        self._validate_analysis_section(_config_fom.analysis_section)
        self._validate_measures_sections(_config_fom)
        self._validate_surroundings_section(_config_fom.surroundings_section)
        self._validate_infrastructure_section(_config_fom.infrastructuur_section)

    def _validate_analysis_section(self, analysis_section: AnalysisSectionFom):
        # Analysis section
        assert isinstance(analysis_section, AnalysisSectionFom)
        # These paths are not included in the test dir so None will be mapped in the FOM.
        assert analysis_section.dike_section_location_shp_file == Path(
            "c:\\fake_drive\\Invoer\\Dijkringlijnen_KOSWAT_2017_WV21_DR10.shp"
        )
        assert analysis_section.dike_selection_txt_file == Path(
            "c:\\fake_drive\\Invoer\\json files\\DijksectieSelectie.txt"
        )
        assert analysis_section.input_profiles_json_dir == Path(
            "c:\\fake_drive\\Invoer\\dike_section_input"
        )
        assert analysis_section.scenarios_json_dir == Path(
            "c:\\fake_drive\\Invoer\\Scenarios"
        )
        # No databaes loaded because the path is not included in the test data.
        assert analysis_section.surroundings_database_dir == Path(
            "c:\\fake_drive\\Invoer\\Omgevingsanalyses"
        )
        assert analysis_section.costs_json_file == Path(
            "c:\\fake_drive\\Invoer\\json files\\Eenheidsprijzen2017.json"
        )
        assert analysis_section.include_taxes == True
        assert analysis_section.analysis_output_dir == Path("c:\\fake_drive\\Uitvoer")
        assert analysis_section.export_measures_png == True
        assert analysis_section.export_layers_png == True
        assert analysis_section.export_shapefiles == True

    def _validate_measures_sections(self, _config_fom: KoswatGeneralJsonFom):
        self._validate_soil_measure_section(_config_fom.soil_reinforcement_section)
        self._validate_soil_waterside_measure_section(
            _config_fom.soil_waterside_reinforcement_section
        )
        self._validate_vertical_piping_solution_section(
            _config_fom.vertical_piping_solution_section
        )
        self._validate_piping_wall_section(_config_fom.piping_wall_section)
        self._validate_stability_wall_toe_section(
            _config_fom.stability_wall_toe_section
        )
        self._validate_stability_wall_crest_section(
            _config_fom.stability_wall_crest_section
        )
        self._validate_cofferdam_section(_config_fom.cofferdam_section)

    def _validate_dike_profile_section(
        self, dike_profile_section: DikeProfileSectionFom
    ):
        # Dijkprofiel section
        assert isinstance(dike_profile_section, DikeProfileSectionFom)
        assert dike_profile_section.thickness_grass_layer == 0.3
        assert dike_profile_section.thickness_clay_layer == 0.5

    def _validate_soil_measure_section(
        self, soil_measure_section: SoilReinforcementSectionFom
    ):
        # Grondmaatregel section
        assert isinstance(soil_measure_section, SoilReinforcementSectionFom)
        assert soil_measure_section.active == True
        assert soil_measure_section.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert (
            soil_measure_section.land_purchase_surtax_factor == SurtaxFactorEnum.NORMAAL
        )
        assert soil_measure_section.min_berm_height == 0.5
        assert soil_measure_section.max_berm_height_factor == 0.4
        assert soil_measure_section.factor_increase_berm_height == 0.05

    def _validate_soil_waterside_measure_section(
        self, soil_waterside_measure_section: SoilWatersideReinforcementSectionFom
    ):
        # Buitendijkse grondmaatregel section
        assert isinstance(
            soil_waterside_measure_section,
            SoilWatersideReinforcementSectionFom,
        )
        assert soil_waterside_measure_section.active == True
        assert (
            soil_waterside_measure_section.soil_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert (
            soil_waterside_measure_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert soil_waterside_measure_section.min_berm_height == 0.5
        assert soil_waterside_measure_section.factor_increase_berm_height == 0.05

    def _validate_vertical_piping_solution_section(
        self, vps_section: VPSReinforcementSectionFom
    ):
        # Verticale piping oplossing section
        assert isinstance(vps_section, VPSReinforcementSectionFom)
        assert vps_section.active == True
        assert vps_section.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert vps_section.constructive_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert vps_section.land_purchase_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert vps_section.polderside_berm_width_vps == 10

    def _validate_piping_wall_section(
        self, piping_wall_section: PipingWallReinforcementSectionFom
    ):
        # Kwelscherm section
        assert isinstance(piping_wall_section, PipingWallReinforcementSectionFom)
        assert piping_wall_section.active == True
        assert piping_wall_section.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert (
            piping_wall_section.constructive_surtax_factor == SurtaxFactorEnum.NORMAAL
        )
        assert (
            piping_wall_section.land_purchase_surtax_factor == SurtaxFactorEnum.NORMAAL
        )
        assert piping_wall_section.min_length_piping_wall == 4
        assert piping_wall_section.transition_cbwall_sheetpile == 99
        assert piping_wall_section.max_length_piping_wall == 25

    def _validate_stability_wall_toe_section(
        self, stability_wall_toe_section: StabilityWallToeReinforcementSectionFom
    ):
        # Stabiliteitswand (teen) section
        assert isinstance(
            stability_wall_toe_section,
            StabilityWallToeReinforcementSectionFom,
        )
        assert stability_wall_toe_section.active == True
        assert (
            stability_wall_toe_section.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        )
        assert (
            stability_wall_toe_section.constructive_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            stability_wall_toe_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert stability_wall_toe_section.steepening_polderside_slope == 3
        assert stability_wall_toe_section.min_length_stability_wall == 5
        assert stability_wall_toe_section.max_length_stability_wall == 15

    def _validate_stability_wall_crest_section(
        self, stability_wall_crest_section: StabilityWallCrestReinforcementSectionFom
    ):
        # Stabiliteitswand (kruin) section
        assert isinstance(
            stability_wall_crest_section,
            StabilityWallCrestReinforcementSectionFom,
        )
        assert stability_wall_crest_section.active == True
        assert (
            stability_wall_crest_section.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        )
        assert (
            stability_wall_crest_section.constructive_surtax_factor
            == SurtaxFactorEnum.NORMAAL
        )
        assert (
            stability_wall_crest_section.land_purchase_surtax_factor
            == SurtaxFactorEnum.MOEILIJK
        )
        assert stability_wall_crest_section.steepening_polderside_slope == 2
        assert stability_wall_crest_section.min_length_stability_wall == 5
        assert stability_wall_crest_section.transition_sheetpile_diaphragm_wall == 20
        assert stability_wall_crest_section.max_length_stability_wall == 25

    def _validate_cofferdam_section(
        self, cofferdam_section: CofferdamReinforcementSectionFom
    ):
        # Kistdam section
        assert isinstance(cofferdam_section, CofferdamReinforcementSectionFom)
        assert cofferdam_section.active == True
        assert cofferdam_section.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert cofferdam_section.constructive_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert cofferdam_section.min_length_cofferdam == 5
        assert cofferdam_section.max_length_cofferdam == 25

    def _validate_surroundings_section(
        self, surroundings_section: SurroundingsSectionFom
    ):
        # Omgeving section
        assert isinstance(surroundings_section, SurroundingsSectionFom)
        assert surroundings_section.construction_distance == 50
        assert surroundings_section.construction_buffer == 10
        assert surroundings_section.allow_waterside_reinforcement is True
        assert surroundings_section.obstacle_types == {"bebouwing": 5}

    def _validate_infrastructure_section(
        self, infrastructure_section: InfrastructureSectionFom
    ):
        # Infrastructuur section
        assert isinstance(infrastructure_section, InfrastructureSectionFom)
        assert infrastructure_section.active == False
        assert infrastructure_section.surtax_factor_roads == SurtaxFactorEnum.NORMAAL
        assert infrastructure_section.infrastructure_costs_0dh == InfraCostsEnum.GEEN
        assert infrastructure_section.buffer_crest_waterside == 0
        assert infrastructure_section.roads_class2_width == 2
        assert infrastructure_section.roads_class24_width == 5
        assert infrastructure_section.roads_class47_width == 8
        assert infrastructure_section.roads_class7_width == 12
        assert infrastructure_section.roads_unknown_width == 8
