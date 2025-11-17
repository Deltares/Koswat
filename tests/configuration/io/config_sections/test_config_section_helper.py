import math
from typing import Optional

import pytest

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class TestConfigSectionHelper:
    @pytest.mark.parametrize(
        "input_val, expected",
        [
            pytest.param(None, None, id="None"),
            pytest.param("input_string", "input_string", id="Value"),
        ],
    )
    def test_get_string_without_default(
        self, input_val: Optional[str], expected: Optional[str]
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_string_without_default(input_val)

        # 2. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            pytest.param(None, "", id="None"),
            pytest.param("input_string", "input_string", id="Value"),
        ],
    )
    def test_get_string(self, input_val: Optional[str], expected: Optional[str]):
        # 1. Execute test
        _result = SectionConfigHelper.get_string(input_val)

        # 2. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            pytest.param(None, None, id="None"),
            pytest.param("MOEILIJK", SurtaxFactorEnum.MOEILIJK, id="Value"),
        ],
    )
    def test_get_enum_without_default(
        self,
        input_val: Optional[str],
        expected: Optional[SurtaxFactorEnum],
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_enum_without_default(input_val)

        # 2. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            pytest.param(None, SurtaxFactorEnum.NORMAAL, id="None"),
            pytest.param("MOEILIJK", SurtaxFactorEnum.MOEILIJK, id="Value"),
        ],
    )
    def test_get_enum(
        self,
        input_val: Optional[str],
        expected: Optional[SurtaxFactorEnum],
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_enum(input_val)

        # 2. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            pytest.param(None, None, id="None"),
            pytest.param("24.42", 24.42, id="String"),
            pytest.param(24.42, 24.42, id="Float"),
        ],
    )
    def test_get_float_without_default(
        self,
        input_val: Optional[str | float],
        expected: Optional[float],
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_float_without_default(input_val)

        # 2. Verify expectations
        assert _result == expected or (math.isnan(_result) and math.isnan(expected))

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            pytest.param(None, math.nan, id="None"),
            pytest.param("24.42", 24.42, id="String"),
            pytest.param(24.42, 24.42, id="Float"),
        ],
    )
    def test_get_float(
        self,
        input_val: Optional[str | float],
        expected: Optional[float],
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_float(input_val)

        # 2. Verify expectations
        assert _result == expected or (math.isnan(_result) and math.isnan(expected))

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            pytest.param(None, None, id="None"),
            pytest.param("True", True, id="String"),
            pytest.param(True, True, id="Boolean"),
        ],
    )
    def test_get_bool_without_default(
        self,
        input_val: Optional[str | bool],
        expected: Optional[float],
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_bool_without_default(input_val)

        # 2. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            pytest.param(None, False, id="None"),
            pytest.param("True", True, id="String"),
            pytest.param(True, True, id="Boolean"),
        ],
    )
    def test_get_bool(
        self,
        input_val: Optional[str | bool],
        expected: Optional[float],
    ):
        # 1. Execute test
        _result = SectionConfigHelper.get_bool(input_val)

        # 2. Verify expectations
        assert _result == expected
