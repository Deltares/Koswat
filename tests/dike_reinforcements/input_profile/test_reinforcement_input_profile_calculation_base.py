from dataclasses import dataclass

import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)


class TestReinforcementInputProfileCalculationBase:
    def test__calculate_new_waterside_slope(self):
        # 1. Define test data.
        _waterside_slope = 3.0
        _scenario = KoswatScenario(waterside_slope=_waterside_slope)

        # 2. Run test.
        _result = (
            ReinforcementInputProfileCalculationBase._calculate_new_waterside_slope(
                None, _scenario
            )
        )

        # 3. Verify expectations
        assert _result == _waterside_slope

    def test__calculate_new_crest_height(self):
        @dataclass
        class MockInputData(KoswatInputProfileProtocol):
            crest_height: float

        # 1. Define test data.
        _input_data = MockInputData(crest_height=6.0)
        _scenario = KoswatScenario(d_h=2)
        _expected_result = 8

        # 2. Run test.
        _result = ReinforcementInputProfileCalculationBase._calculate_new_crest_height(
            _input_data, _scenario
        )

        # 3. Verify expectations
        assert _result == _expected_result

    @pytest.mark.parametrize(
        "berm_height, expected",
        [
            pytest.param(3.0, 8.0, id="berm > ground level"),
            pytest.param(1.0, 1.0, id="berm < ground level"),
        ],
    )
    def test___calculate_new_waterside_berm_height(
        self, berm_height: float, expected: float
    ):
        @dataclass
        class MockInputData(KoswatInputProfileProtocol):
            waterside_ground_level: float
            waterside_berm_height: float

        # 1. Define test data.
        _input_data = MockInputData(
            waterside_ground_level=2.0, waterside_berm_height=berm_height
        )
        _scenario = KoswatScenario(d_h=5.0)

        # 2. Run test.
        _result = ReinforcementInputProfileCalculationBase._calculate_new_waterside_berm_height(
            _input_data, _scenario
        )

        # 3. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "extend_existing, expected",
        [
            pytest.param(True, 2.35, id="Extend existing berm"),
            pytest.param(False, 2.2, id="Do not extend existing berm"),
        ],
    )
    def test__calculate_new_polderside_berm_height_piping(
        self, extend_existing: bool, expected: float
    ):
        @dataclass
        class MockInputData(KoswatInputProfileProtocol):
            polderside_berm_height: float
            polderside_berm_width: float
            polderside_ground_level: float
            crest_height: float

        @dataclass
        class MockSettings(KoswatSoilSettings):
            min_berm_height: float
            max_berm_height_factor: float
            factor_increase_berm_height: float

        # 1. Define test data.
        _input_data = MockInputData(
            polderside_berm_height=5.0,
            polderside_berm_width=6.0,
            polderside_ground_level=1.0,
            crest_height=5.5,
        )
        _soil_settings = MockSettings(
            min_berm_height=1.0,
            max_berm_height_factor=0.3,
            factor_increase_berm_height=0.2,
        )

        # 2. Run test.
        _result = ReinforcementInputProfileCalculationBase._calculate_new_polderside_berm_height_piping(
            _input_data, _input_data, _soil_settings, extend_existing
        )

        # 3. Verify expectations
        assert _result == pytest.approx(expected)
