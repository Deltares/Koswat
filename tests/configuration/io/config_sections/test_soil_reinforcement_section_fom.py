import configparser
import math

from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.io.config_sections.soil_reinforcement_section_fom import (
    SoilReinforcementSectionFom,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum

_test_config = {
    "min_bermhoogte": 2.5,
    "opslagfactor_grond": "MOEILIJK",
}


class TestSoilReinforcementSectionFom:

    def test_from_ini(self):
        # 1. Define test data
        _config_parser = configparser.ConfigParser()
        _config_parser["section"] = _test_config
        _ini_data = _config_parser["section"]

        # 2. Execute test
        _section = SoilReinforcementSectionFom.from_ini(_ini_data)

        # 3. Verify expectations
        assert isinstance(_section, ConfigSectionFomBase)
        assert _section.min_berm_height == 2.5
        assert math.isnan(_section.max_berm_height_factor)
        assert _section.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert _section.land_purchase_surtax_factor == SurtaxFactorEnum.NORMAAL

    def test_from_dict(self):
        # 1. Define test data
        _config_data = _test_config

        # 2. Execute test
        _section = SoilReinforcementSectionFom.from_dict(_config_data)

        # 3. Verify expectations
        assert isinstance(_section, ConfigSectionFomBase)
        assert _section.min_berm_height == 2.5
        assert _section.max_berm_height_factor is None
        assert _section.soil_surtax_factor == SurtaxFactorEnum.MOEILIJK
        assert _section.land_purchase_surtax_factor is None
