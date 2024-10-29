import pytest

from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)


class TestStrategyLocationInput:
    def test_cheapest_reinforcement(
        self, example_location_input: list[StrategyLocationInput]
    ):
        # 1. Run test.
        _cheapest = example_location_input[0].cheapest_reinforcement

        # 2. Verify the final expectations.
        assert _cheapest is not None
        assert isinstance(_cheapest, StrategyReinforcementTypeCosts)

    def test_available_measures(
        self, example_location_input: list[StrategyLocationInput]
    ):
        # 1. Run test.
        _available = example_location_input[0].available_measures

        # 2. Verify the final expectations.
        assert isinstance(_available, list)
        assert any(_available)
        assert isinstance(_available[0], type)

    def test_get_reinforcement_costs(
        self, example_location_input: list[StrategyLocationInput]
    ):
        # 1. Define test data.
        _location_input = example_location_input[0]
        _reinforcement_type = _location_input.available_measures[0]

        # 2. Run test.
        _reinforcement_cost = _location_input.get_reinforcement_costs(
            _reinforcement_type
        )

        # 3. Verify the final expectations.
        assert _reinforcement_cost is not None
        assert isinstance(_reinforcement_cost, float)

    def test_get_reinforcement_costs_raises_value_error(
        self, example_location_input: list[StrategyLocationInput]
    ):
        # 1. Define test data.
        _reinforcement_type = SoilReinforcementProfile

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            example_location_input[-1].get_reinforcement_costs(_reinforcement_type)

        # 3. Verify the final expectations.
        assert str(exc_err.value) == (
            f"Reinforcement {_reinforcement_type.output_name} not available, costs cannot be computed."
        )

    def test_get_infrastructure_costs(
        self, example_location_input: list[StrategyLocationInput]
    ):
        # 1. Define test data.
        _location_input = example_location_input[0]
        _reinforcement_type = _location_input.available_measures[0]

        # 2. Run test.
        _infra_costs = _location_input.get_infrastructure_costs(_reinforcement_type)

        # 3. Verify the final expectations.
        assert _infra_costs is not None
        assert isinstance(_infra_costs, tuple)

    def test_get_infrastructure_costs_raises_value_error(
        self, example_location_input: list[StrategyLocationInput]
    ):
        # 1. Define test data.
        _reinforcement_type = SoilReinforcementProfile

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _infra_costs = example_location_input[-1].get_infrastructure_costs(
                _reinforcement_type
            )

        # 3. Verify the final expectations.
        assert str(exc_err.value) == (
            f"Reinforcement {_reinforcement_type.output_name} not available, costs cannot be computed."
        )
