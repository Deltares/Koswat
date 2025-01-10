import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculated_factors import (
    BermCalculatedFactors,
)


class TestBermCalculatedFactors:
    def test_from_calculation_input_returns_object(
        self,
        valid_input_profile: KoswatInputProfileProtocol,
        valid_scenario: KoswatScenario,
        valid_reinforcement_settings: KoswatReinforcementSettings,
    ):
        # 1. Run test
        _result = BermCalculatedFactors.from_calculation_input(
            base_data=valid_input_profile,
            reinforced_data=valid_input_profile,
            scenario=valid_scenario,
            reinforcement_settings=valid_reinforcement_settings,
        )

        # 2. Verify expectations
        assert isinstance(_result, BermCalculatedFactors)

    @pytest.mark.parametrize(
        "profile_type, expected",
        [
            (InputProfileEnum.STABILITY_WALL, 10.0),
            (InputProfileEnum.VPS, 0.0),
            (InputProfileEnum.NONE, 0.0),
            (None, 0.0),
        ],
    )
    def test_get_dikebasee_piping_new_returns_right_value(
        self, profile_type: InputProfileEnum, expected: float
    ):
        # 1. Define test data
        _calculated_factors = BermCalculatedFactors(
            reinforcement_settings=None,
            scenario=None,
            dikebase_piping_old=None,
            dikebase_piping_new_dict={
                InputProfileEnum.STABILITY_WALL: 10.0,
                InputProfileEnum.SOIL: 5.0,
                InputProfileEnum.NONE: 0.0,
            },
            dikebase_height_new=None,
            dikebase_stability_new=None,
            berm_old_is_stability=None,
            berm_factor_old=None,
            dike_height_new=None,
        )

        # 2. Run test
        _result = _calculated_factors.get_dikebase_piping_new(profile_type)

        # 3. Verify expectations
        assert _result == expected
