from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.koswat_configuration_ini_importer import (
    KoswatConfigurationIniImporter,
)
from koswat.configuration.koswat_configuration import KoswatConfiguration
from tests import test_data


class TestKoswatConfigurationIniImporter:
    def test_koswat_configuration_ini_importer_init(self):
        _builder = KoswatConfigurationIniImporter()
        assert isinstance(_builder, KoswatConfigurationIniImporter)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.ini_configuration

    def test_koswat_configuration_ini_importer_build_from_valid_ini(self):
        # 1. Define test data.
        _ini_file = test_data / "ini_reader" / "koswat_general.ini"
        assert _ini_file.is_file()
        _builder = KoswatConfigurationIniImporter()
        _builder.ini_configuration = _ini_file

        # 2. Run test.
        _config = _builder.build()

        # 3. Verify final expectations.
        assert isinstance(_config, KoswatConfiguration)
        assert _config.is_valid()
