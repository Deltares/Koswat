from hmac import new

import pytest

from koswat.dike_reinforcements.reinforcement_profile.standard.soil_waterside_reinforcement_profile import (
    SoilWatersideReinforcementProfile,
)
from koswat.strategies.criteria.strategy_reinforcement_allowed_waterside_filter_criteria import (
    StrategyReinforcementAllowedWatersideFilterCriteria,
)
from koswat.strategies.strategy_reinforcement_input.strategy_reinforcement_input_protocol import (
    StrategyReinforcementInputProtocol,
)


class TestStrategyReinforcementAllowedWatersideFilterCriteria:

    @pytest.mark.parametrize("allowed_waterside", [True, False])
    def test_when_criteria_met_by_given_reinforcement_profile_is_not_soil_waterside_then_returns_true(
        self, example_strategy_input, allowed_waterside
    ):
        # 1. Define test data
        class MockedStrategyReinforcement(StrategyReinforcementInputProtocol):
            reinforcement_type = 123

        example_strategy_input.waterside_reinforcement_allowed = allowed_waterside

        # 2. When
        result = StrategyReinforcementAllowedWatersideFilterCriteria(
            waterside_reinforcement_allowed=allowed_waterside
        ).criteria_met_by(MockedStrategyReinforcement())

        # Then
        assert result is True

    @pytest.mark.parametrize("allowed_waterside", [True, False])
    def test_when_criteria_met_by_given_soil_waterside_then_returns_expectation(
        self, example_strategy_input, allowed_waterside
    ):
        # 1. Define test data
        class MockedStrategyReinforcement(StrategyReinforcementInputProtocol):
            reinforcement_type = SoilWatersideReinforcementProfile

        example_strategy_input.waterside_reinforcement_allowed = allowed_waterside

        # 2. When
        result = StrategyReinforcementAllowedWatersideFilterCriteria(
            waterside_reinforcement_allowed=allowed_waterside
        ).criteria_met_by(MockedStrategyReinforcement())

        # Then
        assert result is allowed_waterside
