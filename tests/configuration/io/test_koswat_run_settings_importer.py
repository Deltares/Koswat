import math
from pathlib import Path

import pytest

from koswat.configuration.io.json.koswat_dike_section_input_json_reader import (
    KoswatDikeSectionInputJsonReader,
)
from koswat.configuration.io.koswat_run_settings_importer import (
    KoswatRunSettingsImporter,
)
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from tests import test_data, test_data_acceptance


class TestKoswatRunSettingsImporter:
    def test_initialize_importer(self):
        _importer = KoswatRunSettingsImporter()
        assert isinstance(_importer, KoswatRunSettingsImporter)
        assert isinstance(_importer, KoswatImporterProtocol)

    def test_import_dike_section_input_list_without_json_files(self, empty_dir: Path):
        # 1. Define test data.
        _json_folder = empty_dir
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_dike_section_input_list(_json_folder, None)

        # 3. Verify final expectations.
        assert _result == []

    def test_import_dike_section_input_list_missing_folder(self):
        # 1. Define test data.
        _json_folder = Path("non_existing_folder")
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_dike_section_input_list(_json_folder, None)

        # 3. Verify final expectations.
        assert _result == []

    def test_import_selected_dike_section_names_without_txt_file(self, empty_dir: Path):
        # 1. Define test data.
        _txt_file = empty_dir
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_selected_dike_section_names(_txt_file)

        # 3. Verify final expectations.
        assert _result == []

    @pytest.mark.parametrize("include_taxes", [(True), (False)])
    def test_import_dike_costs_without_ini_file(
        self, include_taxes: bool, empty_dir: Path
    ):
        # 1. Define test data.
        _txt_file = empty_dir
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_dike_costs(_txt_file, include_taxes)

        # 3. Verify final expectations.
        assert _result == None

    def test_koswat_run_settings_importer_build_from_valid_ini(self):
        # 1. Define test data.
        _ini_file = test_data.joinpath("acceptance", "koswat_general.ini")
        assert _ini_file.is_file()

        # 2. Run test.
        _config = KoswatRunSettingsImporter().import_from(_ini_file)

        # 3. Verify final expectations.
        assert isinstance(_config.run_scenarios, list)
        assert all(
            isinstance(_rs, KoswatRunScenarioSettings) for _rs in _config.run_scenarios
        )
        assert isinstance(_config.output_dir, Path)

    def test__get_dike_section_input_overrides_defaults(self):
        # 1. Define test data
        _importer = KoswatRunSettingsImporter()
        _general_settings = _importer._import_general_settings(
            test_data.joinpath("section_input", "koswat_general.ini")
        )
        _dike_selection = [
            "all_section_settings",
            "no_section_settings",
            "some_section_settings",
        ]

        # 2. Run test.
        _profiles, _reinforcement_settings_list = _importer._get_dike_section_input(
            _general_settings, _dike_selection
        )

        # 3. Verify final expectations.
        assert len(_profiles) == 3
        assert len(_reinforcement_settings_list) == 3

        # Check that the settings have been overridden correctly

        _reinforcement_settings_keys = dict(
            soil_measure="soil_settings",
            vps="vps_settings",
            piping_wall="piping_wall_settings",
            stability_wall="stability_wall_settings",
            cofferdam="cofferdam_settings",
        )
        for _profile, _reinforcement_settings in zip(
            _profiles, _reinforcement_settings_list
        ):
            assert _profile.input_data.dike_section in _dike_selection

            _section_input_file = (
                _general_settings.analysis_section.input_profiles_json_dir.joinpath(
                    f"{_profile.input_data.dike_section}.json",
                )
            )
            _section_settings = KoswatDikeSectionInputJsonReader().read(
                _section_input_file
            )
            for _config_section, _config_values in _section_settings.__dict__.items():
                if _config_section == "dike_section":
                    assert _profile.input_data.dike_section == _config_values
                elif _config_section == "input_profile":
                    for _key, _value in _config_values.__dict__.items():
                        if _value not in ("", None, math.nan):
                            assert getattr(_profile.input_data, _key) == _value
                else:
                    _reinforcement_settings_section = getattr(
                        _reinforcement_settings,
                        _reinforcement_settings_keys[_config_section],
                    )
                    for _key, _value in _config_values.__dict__.items():
                        if _value not in (None, math.nan):
                            assert (
                                getattr(
                                    _reinforcement_settings_section,
                                    _key,
                                )
                                == _value
                            )
