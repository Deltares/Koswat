import pytest

from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)


class TestStrategyLocationInput:
    def test_cheapest_reinforcement(self, example_strategy_input: StrategyInput):
        # 1. Define test data.
        _location_input = example_strategy_input.strategy_locations[0]

        # 2. Run test.
        _cheapest = _location_input.cheapest_reinforcement

        # 3. Verify the final expectations.
        assert _cheapest is not None
        assert isinstance(_cheapest, StrategyReinforcementTypeCosts)

    def test_available_measures(self, example_strategy_input: StrategyInput):
        # 1. Define test data.
        _location_input = example_strategy_input.strategy_locations[0]

        # 2. Run test.
        _available = _location_input.available_measures

        # 3. Verify the final expectations.
        assert _available is not None
        assert isinstance(_available, list)
        assert len(_available) > 0
        assert isinstance(_available[0], type)

    def test_get_reinforcement_costs(self, example_strategy_input: StrategyInput):
        # 1. Define test data.
        _location_input = example_strategy_input.strategy_locations[0]
        _reinforcement_type = _location_input.available_measures[0]

        # 2. Run test.
        _reinforcement_cost = _location_input.get_reinforcement_costs(
            _reinforcement_type
        )

        # 3. Verify the final expectations.
        assert _reinforcement_cost is not None
        assert isinstance(_reinforcement_cost, float)

    def test_get_reinforcement_costs_raises_value_error(
        self, example_strategy_input: StrategyInput
    ):
        # 1. Define test data.
        _location_input = example_strategy_input.strategy_locations[-1]
        _reinforcement_type = SoilReinforcementProfile

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _location_input.get_reinforcement_costs(_reinforcement_type)

        # 3. Verify the final expectations.
        assert str(exc_err.value) == (
            f"Reinforcement {_reinforcement_type.output_name} not available, costs cannot be computed."
        )

    def test_get_infrastructure_costs(self, example_strategy_input: StrategyInput):
        # 1. Define test data.
        _location_input = example_strategy_input.strategy_locations[0]
        _reinforcement_type = _location_input.available_measures[0]

        # 2. Run test.
        _infra_costs = _location_input.get_infrastructure_costs(_reinforcement_type)

        # 3. Verify the final expectations.
        assert _infra_costs is not None
        assert isinstance(_infra_costs, tuple)

    def test_get_infrastructure_costs_raises_value_error(
        self, example_strategy_input: StrategyInput
    ):
        # 1. Define test data.
        _location_input = example_strategy_input.strategy_locations[-1]
        _reinforcement_type = SoilReinforcementProfile

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _infra_costs = _location_input.get_infrastructure_costs(_reinforcement_type)

        # 3. Verify the final expectations.
        assert str(exc_err.value) == (
            f"Reinforcement {_reinforcement_type.output_name} not available, costs cannot be computed."
        )
