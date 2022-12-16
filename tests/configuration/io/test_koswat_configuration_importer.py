from pathlib import Path

from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.koswat_run_settings_importer import (
    KoswatRunSettingsImporter,
)
from koswat.configuration.settings.koswat_general_settings import *
from koswat.configuration.settings.koswat_run_settings import KoswatRunScenarioSettings
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from tests import test_data


class TestKoswatRunSettingsImporter:
    def test_koswat_run_settings_importer_init(self):
        _builder = KoswatRunSettingsImporter()
        assert isinstance(_builder, KoswatRunSettingsImporter)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.ini_configuration

    def test_koswat_run_settings_importer_build_from_valid_ini(self):
        # 1. Define test data.
        _ini_file = test_data / "acceptance" / "koswat_general.ini"
        assert _ini_file.is_file()
        _builder = KoswatRunSettingsImporter()
        _builder.ini_configuration = _ini_file

        # 2. Run test.
        _config = _builder.build()

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
