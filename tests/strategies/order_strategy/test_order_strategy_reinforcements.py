import math
from typing import Iterator

import pytest

from koswat.dike_reinforcements.reinforcement_profile import (
    CofferdamReinforcementProfile,
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
    VPSReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.order_strategy.order_strategy_reinforcements import (
    OrderStrategyReinforcements,
)
from koswat.strategies.strategy_reinforcement_profile import (
    StrategyReinforcementProfile,
)
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
    ) -> Iterator[list[StrategyReinforcementProfile]]:
        yield [
            StrategyReinforcementProfile(
                reinforcement_type=x, ground_level_surface=10.0 - i, total_cost=i + 1
            )
            for i, x in enumerate(self._default_reinforcements)
        ]

    def test_initialize(
        self,
        order_strategy_reinforcements_fixture: list[StrategyReinforcementProfile],
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
        order_strategy_reinforcements_fixture: list[StrategyReinforcementProfile],
    ):
        # 1. Define test data.
        _strategy_reinforcements = OrderStrategyReinforcements(
            reinforcements=order_strategy_reinforcements_fixture
        )

        # 2. Run test.
        _reinforcements = _strategy_reinforcements.strategy_reinforcements

        # 3. Verify expectations
        assert _reinforcements == self._default_reinforcements
