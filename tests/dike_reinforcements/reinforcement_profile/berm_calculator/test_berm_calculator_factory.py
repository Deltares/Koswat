from dataclasses import dataclass

import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_factory import (
    BermCalculatorFactory,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_protocol import (
    BermCalculatorProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.default_berm_calculator import (
    DefaultBermCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.keep_berm_calculator import (
    KeepBermCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.no_berm_calculator import (
    NoBermCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.piping_berm_calculator import (
    PipingBermCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.stability_berm_calculator import (
    StabilityBermCalculator,
)


class TestBermCalculatorFactory:
    def test_initialize(
        self,
        valid_input_profile: KoswatInputProfileProtocol,
        valid_scenario: KoswatScenario,
        valid_reinforcement_settings: KoswatReinforcementSettings,
    ):
        # 1. Run test
        _result = BermCalculatorFactory(
            base_data=valid_input_profile,
            reinforced_data=valid_input_profile,
            scenario=valid_scenario,
            reinforcement_settings=valid_reinforcement_settings,
        )

        # 2. Verify expectations
        assert isinstance(_result, BermCalculatorFactory)

    @dataclass
    class BermCalculatorCase:
        piping_old: float = 0.0
        piping_new: float = 0.0
        height_new: float = 0.0
        stability_new: float = 0.0
        is_stability: bool = False
        profile_type: InputProfileEnum = InputProfileEnum.NONE
        calculator: type[BermCalculatorProtocol] = None

    calculator_cases = [
        pytest.param(
            BermCalculatorCase(
                calculator=DefaultBermCalculator,
            ),
            id="Default: Default",
        ),
        pytest.param(
            BermCalculatorCase(
                piping_new=10.0,
                height_new=9.0,
                stability_new=8.0,
                calculator=PipingBermCalculator,
            ),
            id="Default: Piping",
        ),
        pytest.param(
            BermCalculatorCase(
                stability_new=10.0,
                height_new=9.0,
                is_stability=True,
                calculator=StabilityBermCalculator,
            ),
            id="Default: Stability",
        ),
        pytest.param(
            BermCalculatorCase(
                stability_new=10.0,
                height_new=9.0,
                calculator=NoBermCalculator,
            ),
            id="Default: No Berm",
        ),
        pytest.param(
            BermCalculatorCase(
                profile_type=InputProfileEnum.COFFERDAM,
                calculator=KeepBermCalculator,
            ),
            id="Cofferdam profile: Keep",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=10.0,
                stability_new=9.0,
                piping_old=8.0,
                profile_type=InputProfileEnum.STABILITY_WALL,
                calculator=NoBermCalculator,
            ),
            id="Stability profile: No Berm 1",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=10.0,
                stability_new=9.0,
                piping_old=11.0,
                profile_type=InputProfileEnum.STABILITY_WALL,
                calculator=PipingBermCalculator,
            ),
            id="Stability profile: Piping",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=9.0,
                stability_new=10.0,
                piping_old=10.0,
                profile_type=InputProfileEnum.STABILITY_WALL,
                is_stability=True,
                calculator=StabilityBermCalculator,
            ),
            id="Stability profile: Stability",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=9.0,
                stability_new=10.0,
                piping_old=10.0,
                profile_type=InputProfileEnum.STABILITY_WALL,
                calculator=NoBermCalculator,
            ),
            id="Stability profile: No Berm 2",
        ),
        pytest.param(
            BermCalculatorCase(
                height_new=10.0,
                stability_new=9.0,
                piping_old=10.0,
                profile_type=InputProfileEnum.STABILITY_WALL,
                calculator=DefaultBermCalculator,
            ),
            id="Stability profile: Default",
        ),
    ]

    @pytest.mark.parametrize("calculator_case", calculator_cases)
    def test_get_berm_calculator_returns_calculator(
        self,
        valid_input_profile: KoswatInputProfileProtocol,
        valid_scenario: KoswatScenario,
        valid_reinforcement_settings: KoswatReinforcementSettings,
        calculator_case: BermCalculatorCase,
    ):
        # 1. Define test data
        _factory = BermCalculatorFactory(
            base_data=valid_input_profile,
            reinforced_data=valid_input_profile,
            scenario=valid_scenario,
            reinforcement_settings=valid_reinforcement_settings,
        )
        _factory._dikebase_piping_old = calculator_case.piping_old
        _factory._dikebase_piping_new_dict[
            calculator_case.profile_type
        ] = calculator_case.piping_new
        _factory._dikebase_height_new = calculator_case.height_new
        _factory._dikebase_stability_new = calculator_case.stability_new
        _factory._berm_old_is_stability = calculator_case.is_stability

        # 2. Run test
        _result = _factory.get_berm_calculator(calculator_case.profile_type)

        # 3. Verify expectations
        assert isinstance(_result, BermCalculatorProtocol)
        assert isinstance(_result, calculator_case.calculator)
