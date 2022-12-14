from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.koswat_run_settings_importer import (
    KoswatRunSettingsImporter,
)
from koswat.configuration.settings.costs.koswat_costs import KoswatCostsSettings
from koswat.configuration.settings.koswat_general_settings import *
from koswat.configuration.settings.koswat_scenario import KoswatScenario
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
        assert isinstance(_config.costs, KoswatCostsSettings)
        assert any(_config.input_profiles)
        assert all((isinstance(_case, KoswatProfileBase) for _case in _config.input_profiles))
        assert _config.output_dir.is_dir()
        assert any(_config.dike_sections)
        # TODO: Work in progress.
        # assert any(_config.scenarios)
        # assert all((isinstance(_case, KoswatScenario) for _case in _config.scenarios))
        # assert any(_config.surroundings)
