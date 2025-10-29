import math
from typing import Optional

import pytest

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class TestConfigSectionHelper:
    @pytest.mark.parametrize(
        "set_defaults, input_val, expected",
        [
            pytest.param(True, None, "", id="None with default"),
            pytest.param(False, None, None, id="None without default"),
            pytest.param(True, "input_string", "input_string", id="Value with default"),
            pytest.param(
                False, "input_string", "input_string", id="Value without default"
            ),
        ],
    )
    def test_get_string(
        self, set_defaults: bool, input_val: Optional[str], expected: Optional[str]
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_string(input_val, set_defaults)

        # 2. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "set_defaults, input_val, expected",
        [
            pytest.param(True, None, SurtaxFactorEnum.NORMAAL, id="None with default"),
            pytest.param(False, None, None, id="None without default"),
            pytest.param(
                True, "MOEILIJK", SurtaxFactorEnum.MOEILIJK, id="Value with default"
            ),
            pytest.param(
                False, "MOEILIJK", SurtaxFactorEnum.MOEILIJK, id="Value without default"
            ),
        ],
    )
    def test_get_enum(
        self,
        set_defaults: bool,
        input_val: Optional[str],
        expected: Optional[SurtaxFactorEnum],
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_enum(input_val, set_defaults)

        # 2. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "set_defaults, input_val, expected",
        [
            pytest.param(True, None, math.nan, id="None with default"),
            pytest.param(False, None, None, id="None without default"),
            pytest.param(True, "24.42", 24.42, id="Value with default"),
            pytest.param(False, "24.42", 24.42, id="Value without default"),
        ],
    )
    def test_get_float(
        self,
        set_defaults: bool,
        input_val: Optional[str],
        expected: Optional[float],
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_float(input_val, set_defaults)

        # 2. Verify expectations
        assert _result == expected or (math.isnan(_result) and math.isnan(expected))
