from dataclasses import dataclass

import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator import (
    BermCalculatorProtocol,
    DefaultBermCalculator,
    KeepBermCalculator,
    NoBermCalculator,
    PipingBermCalculator,
    StabilityBermCalculator,
    WatersideBermCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculated_factors import (
    BermCalculatedFactors,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_factory import (
    BermCalculatorFactory,
)


class TestBermCalculatorFactory:
    @dataclass
    class BermCalculatorCase:
        piping_old: float = 0.0
        piping_new: float = 0.0
        height_new: float = 0.0
        stability_new: float = 0.0
        is_stability: bool = False
        profile_type: InputProfileEnum = InputProfileEnum.NONE
        expected_calculator: type[BermCalculatorProtocol] = None

    calculator_cases = [
        pytest.param(
            BermCalculatorCase(
                expected_calculator=DefaultBermCalculator,
            ),
            id="Default: Default",
        ),
        pytest.param(
            BermCalculatorCase(
                piping_new=10.0,
                height_new=9.0,
                stability_new=8.0,
                expected_calculator=PipingBermCalculator,
            ),
            id="Default: Piping",
        ),
        pytest.param(
            BermCalculatorCase(
                stability_new=10.0,
                height_new=9.0,
                is_stability=True,
                expected_calculator=StabilityBermCalculator,
            ),
            id="Default: Stability",
        ),
        pytest.param(
            BermCalculatorCase(
                stability_new=10.0,
                height_new=9.0,
                expected_calculator=NoBermCalculator,
            ),
            id="Default: No Berm",
        ),
        pytest.param(
            BermCalculatorCase(
                profile_type=InputProfileEnum.COFFERDAM,
                expected_calculator=KeepBermCalculator,
            ),
            id="Cofferdam profile: Keep",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=10.0,
                stability_new=9.0,
                piping_old=8.0,
                profile_type=InputProfileEnum.STABILITY_WALL_CREST,
                expected_calculator=NoBermCalculator,
            ),
            id="Stability profile: No Berm 1",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=10.0,
                stability_new=9.0,
                piping_old=11.0,
                profile_type=InputProfileEnum.STABILITY_WALL_CREST,
                expected_calculator=PipingBermCalculator,
            ),
            id="Stability profile: Piping",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=9.0,
                stability_new=10.0,
                piping_old=10.0,
                profile_type=InputProfileEnum.STABILITY_WALL_CREST,
                is_stability=True,
                expected_calculator=StabilityBermCalculator,
            ),
            id="Stability profile: Stability",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=9.0,
                stability_new=10.0,
                piping_old=10.0,
                profile_type=InputProfileEnum.STABILITY_WALL_CREST,
                expected_calculator=NoBermCalculator,
            ),
            id="Stability profile: No Berm 2",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=10.0,
                stability_new=9.0,
                piping_old=10.0,
                profile_type=InputProfileEnum.STABILITY_WALL_CREST,
                expected_calculator=DefaultBermCalculator,
            ),
            id="Stability profile: Default",
        ),
    ]

    @pytest.mark.parametrize("calculator_case", calculator_cases)
    def test_get_polderside_berm_calculator_returns_calculator(
        self,
        valid_scenario: KoswatScenario,
        valid_reinforcement_settings: KoswatReinforcementSettings,
        calculator_case: BermCalculatorCase,
    ):
        # 1. Define test data
        _factors = BermCalculatedFactors(
            reinforcement_settings=valid_reinforcement_settings,
            scenario=valid_scenario,
            dikebase_piping_old=calculator_case.piping_old,
            dikebase_piping_new_dict={
                calculator_case.profile_type: calculator_case.piping_new,
            },
            dikebase_height_new=calculator_case.height_new,
            dikebase_stability_new=calculator_case.stability_new,
            berm_old_is_stability=calculator_case.is_stability,
            berm_factor_old=None,
            dike_height_new=None,
        )

        # 2. Run test
        _result = BermCalculatorFactory.get_polderside_berm_calculator(
            calculator_case.profile_type, _factors
        )

        # 3. Verify expectations
        assert isinstance(_result, BermCalculatorProtocol)
        assert isinstance(_result, calculator_case.expected_calculator)

    def test_when_get_waterside_berm_calculator_then_waterside_berm_calculator_returned(
        self,
        valid_scenario: KoswatScenario,
        valid_reinforcement_settings: KoswatReinforcementSettings,
    ):
        # 1. Define test data
        _factors = BermCalculatedFactors(
            reinforcement_settings=valid_reinforcement_settings,
            scenario=valid_scenario,
            dikebase_piping_old=0.0,
            dikebase_piping_new_dict={
                InputProfileEnum.SOIL_WATERSIDE: 0.0,
            },
            dikebase_height_new=0.0,
            dikebase_stability_new=0.0,
            berm_old_is_stability=False,
            berm_factor_old=0.0,
            dike_height_new=0.0,
        )

        # 2. Run test
        _result = BermCalculatorFactory.get_waterside_berm_calculator(
            InputProfileEnum.SOIL_WATERSIDE, _factors
        )

        # 3. Verify expectations
        assert isinstance(_result, BermCalculatorProtocol)
        assert isinstance(_result, WatersideBermCalculator)
        assert _result.dikebase_piping_new == 0.0
