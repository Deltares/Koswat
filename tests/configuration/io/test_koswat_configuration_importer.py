from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.koswat_settings_importer import KoswatSettingsFomImporter
from koswat.configuration.settings.koswat_general_settings import *
from tests import test_data


class TestKoswatConfigurationImporter:
    def test_koswat_configuration_importer_init(self):
        _builder = KoswatSettingsFomImporter()
        assert isinstance(_builder, KoswatSettingsFomImporter)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.ini_configuration

    def test_koswat_configuration_importer_build_from_valid_ini(self):
        # 1. Define test data.
        _ini_file = test_data / "acceptance" / "koswat_general.ini"
        assert _ini_file.is_file()
        _builder = KoswatSettingsFomImporter()
        _builder.ini_configuration = _ini_file

        # 2. Run test.
        _config = _builder.build()

        # 3. Verify final expectations.
        assert isinstance(_config, KoswatGeneralSettings)
        assert isinstance(_config.analysis_settings, AnalysisSettings)
        assert isinstance(_config.dike_profile_settings, DikeProfileSettings)
        assert isinstance(_config.soil_settings, SoilSettings)
        assert isinstance(_config.pipingwall_settings, PipingwallSettings)
        assert isinstance(_config.stabilitywall_settings, StabilitywallSettings)
        assert isinstance(_config.cofferdam_settings, CofferdamSettings)
        assert isinstance(_config.infrastructure_settings, InfrastructuurSettings)
        assert isinstance(_config.surroundings_settings, SurroundingsSettings)
        assert _config.is_valid()
