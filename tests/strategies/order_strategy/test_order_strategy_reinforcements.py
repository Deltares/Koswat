from typing import Iterator

import pytest

from koswat.dike_reinforcements.reinforcement_profile import (
    CofferdamReinforcementProfile,
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
    VPSReinforcementProfile,
)
from koswat.strategies.order_strategy.order_strategy_reinforcements import (
    OrderStrategyReinforcements,
)
from koswat.strategies.strategy_reinforcement_type import StrategyReinforcementType
from koswat.strategies.strategy_reinforcements_protocol import (
    StrategyReinforcementsProtocol,
)


class TestOrderStrategyReinforcements:
    _default_reinforcements = [
        SoilReinforcementProfile,
        VPSReinforcementProfile,
        PipingWallReinforcementProfile,
        StabilityWallReinforcementProfile,
        CofferdamReinforcementProfile,
    ]

    @pytest.fixture(name="order_strategy_reinforcements_fixture")
    def _get_order_strategy_reinforcements(
        self,
    ) -> Iterator[list[StrategyReinforcementType]]:
        yield [
            StrategyReinforcementType(
                reinforcement_type=x,
                base_costs=i + 1,
                infastructure_costs=0.0,
                ground_level_surface=10.0 - i,
            )
            for i, x in enumerate(self._default_reinforcements)
        ]

    def test_initialize(
        self,
        order_strategy_reinforcements_fixture: list[StrategyReinforcementType],
    ):
        # 1. Define test data.

        # 2. Run test.
        _strategy_reinforcements = OrderStrategyReinforcements(
            reinforcements=order_strategy_reinforcements_fixture
        )

        # 3. Verify expectations
        assert isinstance(_strategy_reinforcements, OrderStrategyReinforcements)
        assert isinstance(_strategy_reinforcements, StrategyReinforcementsProtocol)

    def test_get_default_order(self):
        # 1. Define test data.

        # 2. Run test.
        _reinforcements = OrderStrategyReinforcements.get_default_order()

        # 3. Verify expectations
        assert _reinforcements == self._default_reinforcements

    def test_strategy_reinforcements(
        self,
        order_strategy_reinforcements_fixture: list[StrategyReinforcementType],
    ):
        # 1. Define test data.
        _strategy_reinforcements = OrderStrategyReinforcements(
            reinforcements=order_strategy_reinforcements_fixture
        )

        # 2. Run test.
        _reinforcements = _strategy_reinforcements.strategy_reinforcements

        # 3. Verify expectations
        assert _reinforcements == self._default_reinforcements
