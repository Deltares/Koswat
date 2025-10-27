import configparser
import math

from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class TestConfigSectionFomBase:
    class DummyConfigSection(ConfigSectionFomBase):
        some_bool: bool
        other_bool: bool
        some_float: float
        other_float: float
        some_surtax: SurtaxFactorEnum
        other_surtax: SurtaxFactorEnum

        _bool_mappings = dict(
            bool_one="some_bool",
            bool_two="other_bool",
        )
        _float_mappings = dict(
            float_one="some_float",
            float_two="other_float",
        )
        _surtax_mappings = dict(
            surtax_one="some_surtax",
            surtax_two="other_surtax",
        )

        @staticmethod
        def get_test_data_dict():
            return {
                "bool_one": True,
                "float_one": "2.5",
                "surtax_one": "Moeilijk",
            }

    def test_from_ini(self):
        # 1. Define test data
        _config_parser = configparser.ConfigParser()
        _config_parser["section"] = self.DummyConfigSection.get_test_data_dict()
        _ini_data = _config_parser["section"]

        # 2. Execute test
        _section = self.DummyConfigSection.from_ini(_ini_data)

        # 3. Verify expectations
        assert isinstance(_section, self.DummyConfigSection)
        assert isinstance(_section, ConfigSectionFomBase)
        assert _section.some_float == 2.5
        assert _section.other_float is math.nan
        assert _section.some_surtax == SurtaxFactorEnum.MOEILIJK
        assert _section.other_surtax is SurtaxFactorEnum.NORMAAL

    def test_from_dict(self):
        # 1. Define test data
        _ini_data = self.DummyConfigSection.get_test_data_dict()

        # 2. Execute test
        _section = self.DummyConfigSection.from_dict(_ini_data)

        # 3. Verify expectations
        assert isinstance(_section, self.DummyConfigSection)
        assert isinstance(_section, ConfigSectionFomBase)
        assert _section.some_float == 2.5
        assert _section.other_float is None
        assert _section.some_surtax == SurtaxFactorEnum.MOEILIJK
        assert _section.other_surtax is None
