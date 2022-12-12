from koswat.builder_protocol import BuilderProtocol
from koswat.configuration.io.koswat_configuration_importer import (
    KoswatConfigurationImporter,
)
from koswat.configuration.koswat_configuration import KoswatConfiguration
from koswat.configuration.models import KoswatCosts, KoswatDikeSelection, KoswatScenario
from tests import test_data


class TestKoswatConfigurationImporter:
    def test_koswat_configuration_importer_init(self):
        _builder = KoswatConfigurationImporter()
        assert isinstance(_builder, KoswatConfigurationImporter)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.ini_configuration

    def test_koswat_configuration_importer_build_from_valid_ini(self):
        # 1. Define test data.
        _ini_file = test_data / "acceptance" / "koswat_general.ini"
        assert _ini_file.is_file()
        _builder = KoswatConfigurationImporter()
        _builder.ini_configuration = _ini_file

        # 2. Run test.
        _config = _builder.build()

        # 3. Verify final expectations.
        assert isinstance(_config, KoswatConfiguration)
        assert any(_config.scenarios)
        assert all(
            isinstance(_scenario, KoswatScenario) for _scenario in _config.scenarios
        )
        assert isinstance(_config.costs, KoswatCosts)
        assert isinstance(_config.dike_sections, KoswatDikeSelection)
        assert _config.is_valid()
