import json
import math
from operator import ge
from pathlib import Path
from typing import Callable, Iterable, Iterator, Tuple

import pytest

from koswat.configuration.io.config_sections.dike_profile_section_fom import DikeProfileSectionFom
from koswat.configuration.io.json.koswat_dike_section_input_json_reader import (
    KoswatDikeSectionInputJsonReader,
)
from koswat.configuration.io.json.koswat_general_json_fom import KoswatGeneralJsonFom
from koswat.configuration.io.koswat_run_settings_importer import (
    KoswatRunSettingsImporter,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.configuration.settings.koswat_run_settings import KoswatRunSettings
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import KoswatReinforcementSettings
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from tests import test_data, test_results


class TestKoswatRunSettingsImporter:
    def test_when_initialize_importer_then_expected_instance_returned(self):
        _importer = KoswatRunSettingsImporter()
        assert isinstance(_importer, KoswatRunSettingsImporter)
        assert isinstance(_importer, KoswatImporterProtocol)

    def test_when__import_dike_section_input_list_given_no_json_files_then_empty_result_list(self, empty_dir: Path):
        # 1. Define test data.
        _json_folder = empty_dir
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_dike_section_input_list(_json_folder, None)

        # 3. Verify final expectations.
        assert _result == []

    def test_when__import_dike_section_input_list_given_missing_folder_then_empty_result_list(self):
        # 1. Define test data.
        _json_folder = Path("non_existing_folder")
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_dike_section_input_list(_json_folder, None)

        # 3. Verify final expectations.
        assert _result == []

    def test_when__import_selected_dike_section_names_given_no_txt_file_then_empty_result_list(
        self, empty_dir: Path
    ):
        # 1. Define test data.
        _txt_file = empty_dir.joinpath("non_existing_file.txt")
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_selected_dike_section_names(_txt_file)

        # 3. Verify final expectations.
        assert _result == []

    def test_when__import_selected_dike_section_names_given_empty_txt_file_then_empty_result_list(
        self, empty_file: Path
    ):
        # 1. Define test data.
        _txt_file = empty_file
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_selected_dike_section_names(_txt_file)

        # 3. Verify final expectations.
        assert _result == []

    @pytest.mark.parametrize("include_taxes", [(True), (False)])
    def test_when__import_dike_costs_given_no_json_file_then_returns_none(
        self, include_taxes: bool, empty_dir: Path
    ):
        # 1. Define test data.
        _txt_file = empty_dir
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_dike_costs(_txt_file, include_taxes)

        # 3. Verify final expectations.
        assert _result == None

    def test_when_import_from_given_valid_json_then_returns_expected_config_instance(self):
        # 1. Define test data.
        _config_file = test_data.joinpath("acceptance", "koswat_general.json")
        assert _config_file.is_file()

        # 2. Run test.
        _config = KoswatRunSettingsImporter().import_from(_config_file)

        # 3. Verify final expectations.
        assert isinstance(_config, KoswatRunSettings)
        assert isinstance(_config.run_scenarios, list)
        assert all(
            isinstance(_rs, KoswatRunScenarioSettings) for _rs in _config.run_scenarios
        )
        assert isinstance(_config.output_dir, Path)

    def test_when_import_from_given_no_dike_sections_then_run_scenarios_is_empty(
        self, empty_file: Path
    ):
        # 1. Define test data
        # Overwrite section selection with empty file
        _config_file = test_data.joinpath("acceptance", "koswat_general.json")
        _temp_file = test_results.joinpath("koswat_general_temp.json")
        _config = json.loads(_config_file.read_text(encoding="utf8"))
        _config["Analyse"]["Dijksecties_Selectie"] = str(empty_file)
        with open(_temp_file, "w", encoding="utf8") as _file:
            json.dump(_config, _file, indent=4)

        assert _temp_file.is_file()

        # 2. Run test
        _config = KoswatRunSettingsImporter().import_from(_temp_file)

        # 3. Verify expectations
        assert isinstance(_config, KoswatRunSettings)
        assert _config.run_scenarios == []

    @pytest.fixture(name="general_settings")
    def _get_valid_general_settings(self) -> KoswatGeneralJsonFom:
        _importer = KoswatRunSettingsImporter()
        return _importer._import_general_settings(
            test_data.joinpath("section_input", "koswat_general.json")
        )

    def _compare_settings_as_dict(self, settings_a: dict[str, float], settings_b: dict[str, float], except_keys: list[str]) -> None:
        for _key in filter(lambda k: k not in except_keys, settings_a.keys()):
            assert settings_a[_key] == settings_b[_key]


    @pytest.fixture(name="general_settings_dike_profile")
    def _get_valid_general_settings_dike_profile(self, general_settings: KoswatGeneralJsonFom) -> Tuple[KoswatGeneralJsonFom, Callable[[DikeProfileSectionFom, KoswatReinforcementSettings], None]]:
        assert general_settings.dike_profile_section.waterside_slope == 3.52
        assert general_settings.dike_profile_section.waterside_berm_height == 0.6
        assert general_settings.dike_profile_section.waterside_ground_level == 0.6
        assert general_settings.dike_profile_section.waterside_berm_width == 0.0
        assert general_settings.dike_profile_section.crest_height == 4.21
        assert general_settings.dike_profile_section.crest_width == 3.97
        assert general_settings.dike_profile_section.polderside_ground_level == 2.82
        assert general_settings.dike_profile_section.polderside_slope == 2.4
        assert general_settings.dike_profile_section.polderside_berm_height == 2.82
        assert general_settings.dike_profile_section.polderside_berm_width == 0.0
        assert general_settings.dike_profile_section.ground_price_builtup == 176.62
        assert general_settings.dike_profile_section.ground_price_unbuilt == 9.22
        assert general_settings.dike_profile_section.factor_settlement == 1.2
        assert general_settings.dike_profile_section.pleistocene == -5.06
        assert general_settings.dike_profile_section.aquifer == -2.06
        assert general_settings.dike_profile_section.thickness_cover_layer == 3.0
        assert general_settings.dike_profile_section.thickness_grass_layer == 0.3
        assert general_settings.dike_profile_section.thickness_clay_layer == 0.5

        def settings_comparison(profile: DikeProfileSectionFom, reinforcement_settings: KoswatReinforcementSettings) -> None:
            _generated_profile = profile.input_data
            self._compare_settings_as_dict(
                general_settings.dike_profile_section.__dict__,
                _generated_profile.__dict__, 
                except_keys=["dike_section", "polderside_ground_level", "thickness_grass_layer"])
            assert _generated_profile.polderside_ground_level == 2.81
            assert _generated_profile.thickness_grass_layer == 0.31
        
        return general_settings, settings_comparison
        
    @pytest.fixture(name="general_settings_soil_measurement")
    def _get_valid_general_settings_soil_measurement(self, general_settings: KoswatGeneralJsonFom) -> Tuple[KoswatGeneralJsonFom, Callable[[DikeProfileSectionFom, KoswatReinforcementSettings], None]]:
        _soil_settings = general_settings.soil_measure_section
        assert _soil_settings.active == True
        assert _soil_settings.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _soil_settings.land_purchase_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _soil_settings.min_berm_height == 0.5
        assert _soil_settings.max_berm_height_factor == 0.4
        assert _soil_settings.factor_increase_berm_height == 0.05
        
        def settings_comparison(profile: DikeProfileSectionFom, reinforcement_settings: KoswatReinforcementSettings) -> None:
            self._compare_settings_as_dict(
                _soil_settings.__dict__,
                reinforcement_settings.soil_settings.__dict__,
                except_keys=["soil_surtax_factor"])
            assert reinforcement_settings.soil_settings.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        
        return general_settings, settings_comparison

    @pytest.fixture(name="general_settings_vps_measurement")
    def _get_valid_general_settings_vps_measurement(self, general_settings: KoswatGeneralJsonFom) -> Tuple[KoswatGeneralJsonFom, Callable[[DikeProfileSectionFom, KoswatReinforcementSettings], None]]:
        _vps_settings = general_settings.vps_section
        assert _vps_settings.active == True
        assert _vps_settings.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _vps_settings.land_purchase_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _vps_settings.constructive_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _vps_settings.polderside_berm_width_vps == 10
        
        def settings_comparison(profile: DikeProfileSectionFom, reinforcement_settings: KoswatReinforcementSettings) -> None:
            self._compare_settings_as_dict(
                _vps_settings.__dict__,
                reinforcement_settings.vps_settings.__dict__,
                except_keys=["active", "polderside_berm_width_vps"])
            assert reinforcement_settings.vps_settings.active == False
            assert reinforcement_settings.vps_settings.polderside_berm_width_vps == 11

        return general_settings, settings_comparison

    @pytest.fixture(name="general_settings_piping_wall_measurement")
    def _get_valid_general_settings_piping_wall_measurement(self, general_settings: KoswatGeneralJsonFom) -> Tuple[KoswatGeneralJsonFom, Callable[[DikeProfileSectionFom, KoswatReinforcementSettings], None]]:
        _settings = general_settings.piping_wall_section
        assert _settings.active == True
        assert _settings.soil_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _settings.land_purchase_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _settings.constructive_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _settings.min_length_piping_wall == 4
        assert _settings.max_length_piping_wall == 25
        assert _settings.transition_cbwall_sheetpile == 99
        
        def settings_comparison(profile: DikeProfileSectionFom, reinforcement_settings: KoswatReinforcementSettings) -> None:
            self._compare_settings_as_dict(
                _settings.__dict__,
                reinforcement_settings.piping_wall_settings.__dict__,
                except_keys=["min_length_piping_wall", "max_length_piping_wall", "transition_cbwall_sheetpile"])
            assert reinforcement_settings.piping_wall_settings.min_length_piping_wall == 5
            assert reinforcement_settings.piping_wall_settings.max_length_piping_wall == 30
            assert reinforcement_settings.piping_wall_settings.transition_cbwall_sheetpile == 95
        return general_settings, settings_comparison

    @pytest.fixture(name="general_settings_stability_wall_toe_measurement")
    def _get_valid_general_settings_stability_wall_toe_measurement(self, general_settings: KoswatGeneralJsonFom) -> Tuple[KoswatGeneralJsonFom, Callable[[DikeProfileSectionFom, KoswatReinforcementSettings], None]]:
        _settings = general_settings.stability_wall_toe_section
        assert _settings.active == True
        assert _settings.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert _settings.land_purchase_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert _settings.constructive_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _settings.min_length_stability_wall == 5
        assert _settings.max_length_stability_wall == 15
        assert _settings.steepening_polderside_slope == 3
        
        def settings_comparison(profile: DikeProfileSectionFom, reinforcement_settings: KoswatReinforcementSettings) -> None:
            self._compare_settings_as_dict(
                _settings.__dict__,
                reinforcement_settings.stability_wall_toe_settings.__dict__,
                except_keys=[])

        return general_settings, settings_comparison

    @pytest.fixture(name="general_settings_stability_wall_crest_measurement")
    def _get_valid_general_settings_stability_wall_crest_measurement(self, general_settings: KoswatGeneralJsonFom) -> Tuple[KoswatGeneralJsonFom, Callable[[DikeProfileSectionFom, KoswatReinforcementSettings], None]]:
        _settings = general_settings.stability_wall_crest_section
        assert _settings.active == True
        assert _settings.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert _settings.land_purchase_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert _settings.constructive_surtax_factor == SurtaxFactorEnum.NORMAAL
        assert _settings.min_length_stability_wall == 5
        assert _settings.max_length_stability_wall == 25
        assert _settings.transition_sheetpile_diaphragm_wall == 20
        assert _settings.steepening_polderside_slope == 2
        
        def settings_comparison(profile: DikeProfileSectionFom, reinforcement_settings: KoswatReinforcementSettings) -> None:
            self._compare_settings_as_dict(
                _settings.__dict__,
                reinforcement_settings.stability_wall_crest_settings.__dict__,
                except_keys=[])

        return general_settings, settings_comparison

    @pytest.fixture(name="general_settings_cofferdam_measurement")
    def _get_valid_general_settings_cofferdam_measurement(self, general_settings: KoswatGeneralJsonFom) -> Tuple[KoswatGeneralJsonFom, Callable[[DikeProfileSectionFom, KoswatReinforcementSettings], None]]:
        _settings = general_settings.cofferdam_section
        assert _settings.active == True
        assert _settings.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert _settings.constructive_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert _settings.min_length_cofferdam == 5
        assert _settings.max_length_cofferdam == 25
        
        def settings_comparison(profile: DikeProfileSectionFom, reinforcement_settings: KoswatReinforcementSettings) -> None:
            self._compare_settings_as_dict(
                _settings.__dict__,
                reinforcement_settings.cofferdam_settings.__dict__,
                except_keys=["soil_surtax_factor", "max_length_cofferdam"])
            assert reinforcement_settings.cofferdam_settings.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
            assert reinforcement_settings.cofferdam_settings.max_length_cofferdam == 26
        return general_settings, settings_comparison
    
    @pytest.fixture(name="general_settings_surroundings")
    def _get_valid_general_settings_surroundings(self, general_settings: KoswatGeneralJsonFom) -> Tuple[KoswatGeneralJsonFom, Callable[[DikeProfileSectionFom, KoswatReinforcementSettings], None]]:
        assert general_settings.surroundings_section.allow_waterside_reinforcement == True
        def settings_comparison(profile: DikeProfileSectionFom, reinforcement_settings: KoswatReinforcementSettings) -> None:
            assert reinforcement_settings.allow_waterside_reinforcement == False
        return general_settings, settings_comparison

    @pytest.mark.parametrize("fixture_name", [
        pytest.param("general_settings_dike_profile", id="dike_profile"),
        pytest.param("general_settings_soil_measurement", id="soil_measurement"),
        pytest.param("general_settings_vps_measurement", id="vps_measurement"),
        pytest.param("general_settings_piping_wall_measurement", id="piping_wall_measurement"),
        pytest.param("general_settings_stability_wall_toe_measurement", id="stability_wall_toe_measurement"),
        pytest.param("general_settings_stability_wall_crest_measurement", id="stability_wall_crest_measurement"),
        pytest.param("general_settings_cofferdam_measurement", id="cofferdam_measurement"),
        pytest.param("general_settings_surroundings", id="surroundings")
    ])
    def test_when__get_dike_section_input_given_custom_section_settings_then_general_settings_are_overriden(self, fixture_name: str, request: pytest.FixtureRequest) -> None:
        # 1. Define test data.
        _dike_selection = [
            "some_section_settings",
        ]        
        _settings, _settings_comparison = request.getfixturevalue(fixture_name)
        
        # 2. Run test.
        _profiles, _reinforcement_settings_list = KoswatRunSettingsImporter()._get_dike_section_input(
            _settings, _dike_selection
        )

        # 3. Verify expectations
        assert len(_profiles) == 1
        assert len(_reinforcement_settings_list) == 1
        _settings_comparison(_profiles[0], _reinforcement_settings_list[0])

