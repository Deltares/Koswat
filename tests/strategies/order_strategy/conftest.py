import pytest

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_waterside_reinforcement_profile import (
    SoilWatersideReinforcementProfile,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_reinforcement_input.strategy_reinforcement_input_protocol import (
    StrategyReinforcementInputProtocol,
)


@pytest.fixture(name="example_default_order", scope="session")
def _get_example_default_order() -> list[type[ReinforcementProfileProtocol]]:
    _reinforcement_order = OrderStrategy.get_default_order_for_reinforcements()
    return _exclude_waterside_soil_reinforcement(_reinforcement_order)


def _exclude_waterside_soil_reinforcement(
    strategy_reinforcements: list[StrategyReinforcementInputProtocol],
) -> list[StrategyReinforcementInputProtocol]:
    _idx = strategy_reinforcements.index(SoilWatersideReinforcementProfile)
    strategy_reinforcements.pop(_idx)
    return strategy_reinforcements
