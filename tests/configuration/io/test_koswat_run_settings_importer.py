from pathlib import Path

import pytest

from koswat.configuration.io.koswat_run_settings_importer import (
    KoswatRunSettingsImporter,
)
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from tests import test_data


class TestKoswatRunSettingsImporter:
    def test_initialize_importer(self):
        _importer = KoswatRunSettingsImporter()
        assert isinstance(_importer, KoswatRunSettingsImporter)
        assert isinstance(_importer, KoswatImporterProtocol)

    def test_import_dike_input_profiles_lists_without_csv_file(self):
        # 1. Define test data.
        _csv_file = Path(__file__).parent
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_dike_input_profiles_list(_csv_file, None, None)

        # 3. Verify final expectations.
        assert _result == []

    def test_import_selected_dike_section_names_without_txt_file(self):
        # 1. Define test data.
        _txt_file = Path(__file__).parent
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_selected_dike_section_names(_txt_file)

        # 3. Verify final expectations.
        assert _result == []

    @pytest.mark.parametrize("include_taxes", [(True), (False)])
    def test_import_dike_costs_without_ini_file(self, include_taxes: bool):
        # 1. Define test data.
        _txt_file = Path(__file__).parent
        _importer = KoswatRunSettingsImporter()

        # 2. Run test.
        _result = _importer._import_dike_costs(_txt_file, include_taxes)

        # 3. Verify final expectations.
        assert _result == None

    def test_koswat_run_settings_importer_build_from_valid_ini(self):
        # 1. Define test data.
        _ini_file = test_data / "acceptance" / "koswat_general.ini"
        assert _ini_file.is_file()

        # 2. Run test.
        _config = KoswatRunSettingsImporter().import_from(_ini_file)

        # 3. Verify final expectations.
        assert isinstance(_config.run_scenarios, list)
        assert all(
            isinstance(_rs, KoswatRunScenarioSettings) for _rs in _config.run_scenarios
        )
        assert isinstance(_config.input_profile_cases, list)
        assert all(
            isinstance(_pc, KoswatProfileBase) for _pc in _config.input_profile_cases
        )
        assert isinstance(_config.output_dir, Path)
