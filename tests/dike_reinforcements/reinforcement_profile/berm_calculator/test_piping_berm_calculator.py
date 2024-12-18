import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.piping_berm_calculator import (
    PipingBermCalculator,
)


class TestPipingBermCalculator:
    @pytest.mark.parametrize(
        "piping_old, piping_new, height_new, stability_new, expected",
        [
            pytest.param(
                15.0, 20.0, 11.0, 10.0, (9.0, 2.0, 1.34), id="Extend existing berm"
            ),
            pytest.param(
                25.0, 20.0, 11.0, 10.0, (9.0, 2.0, 1.34), id="Keep existing berm"
            ),
        ],
    )
    def test_calculate(
        self,
        valid_scenario: KoswatScenario,
        valid_reinforcement_settings: KoswatReinforcementSettings,
        valid_input_profile: KoswatInputProfileProtocol,
        piping_old: float,
        piping_new: float,
        height_new: float,
        stability_new: float,
        expected: tuple[float, float, float],
    ):
        # 1. Define test data
        _calculator = PipingBermCalculator(
            scenario=valid_scenario,
            reinforcement_settings=valid_reinforcement_settings,
            dikebase_piping_old=piping_old,
            dikebase_piping_new=piping_new,
            dikebase_height_new=height_new,
            dikebase_stability_new=stability_new,
            dike_height_new=0.0,
        )

        # 2. Run test
        _result = _calculator.calculate(
            base_data=valid_input_profile,
            reinforced_data=valid_input_profile,
        )

        # 3. Verify expectations
        assert isinstance(_result, tuple)
        assert len(_result) == 3
        assert all(isinstance(_, float) for _ in _result)
        assert all(a == pytest.approx(b) for a, b in zip(_result, expected))
