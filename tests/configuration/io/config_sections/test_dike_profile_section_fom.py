import configparser
import math

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
)
from koswat.configuration.io.config_sections.dike_profile_section_fom import (
    DikeProfileSectionFom,
)

_test_config = {
    "dijkvak": "vak_1",
    "buiten_maaiveld": "-1.5",
}


class TestDikeProfileSectionFom:

    def test_from_config(self):
        # 1. Define test data
        _config_data = _test_config

        # 2. Execute test
        _section = DikeProfileSectionFom.from_config(_config_data, set_defaults=False)

        # 3. Verify expectations
        assert isinstance(_section, ConfigSectionFomProtocol)
        assert _section.dike_section == "vak_1"
        assert _section.waterside_ground_level == -1.5
        assert _section.waterside_berm_height is None

    def test_from_config_set_defaults(self):
        # 1. Define test data
        _config_parser = configparser.ConfigParser()
        _config_parser["section"] = _test_config
        _ini_data = _config_parser["section"]

        # 2. Execute test
        _section = DikeProfileSectionFom.from_config(dict(_ini_data), set_defaults=True)

        # 3. Verify expectations
        assert isinstance(_section, ConfigSectionFomProtocol)
        assert _section.dike_section == "vak_1"
        assert _section.waterside_ground_level == -1.5
        assert math.isnan(_section.waterside_berm_height)
