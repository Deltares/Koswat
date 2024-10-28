from __future__ import annotations

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
from koswat.strategies.order_strategy.order_strategy_buffering import (
    OrderStrategyBuffering,
)
from koswat.strategies.order_strategy.order_strategy_clustering import (
    OrderStrategyClustering,
)
from koswat.strategies.strategy_input import StrategyInput, StrategyLocationInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_protocol import StrategyProtocol


class OrderStrategy(StrategyProtocol):
    @staticmethod
    def get_default_order_for_reinforcements() -> list[
        type[ReinforcementProfileProtocol]
    ]:
        """
        Give the default order for reinforcements types,
        assuming they are sorted from cheapest to most expensive
        and least restrictive to most restrictive.

        Returns:
            list[type[ReinforcementProfileProtocol]]: list of reinforcement types
        """
        return [
            SoilReinforcementProfile,
            VPSReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]

    def get_strategy_order_for_reinforcements(
        self,
    ) -> list[type[ReinforcementProfileProtocol]]:
        """
        Give the ordered reinforcement types for this strategy,
        from cheapest to most expensive,
        possibly omitting reinforcement types that are more expensive and more restrictive than others.
        Cofferdam should always be the last reinforcement type.

        Returns:
            list[type[ReinforcementProfileProtocol]]: list of reinforcement types
        """
        # TODO Implement this method
        return self.get_default_order_for_reinforcements()

    @staticmethod
    def get_strategy_reinforcements(
        strategy_locations: list[StrategyLocationInput],
        selection_order: list[type[ReinforcementProfileProtocol]],
    ) -> list[StrategyLocationReinforcement]:
        _strategy_reinforcements = []
        for _strategy_location in strategy_locations:
            _reinforcements = _strategy_location.available_measures
            _selected_reinforcement = next(
                (_or for _or in selection_order if _or in _reinforcements),
                selection_order[-1],
            )
            _strategy_reinforcements.append(
                StrategyLocationReinforcement(
                    location=_strategy_location.point_surrounding,
                    available_measures=_reinforcements,
                    selected_measure=_selected_reinforcement,
                    strategy_location_input=_strategy_location,
                )
            )
        return _strategy_reinforcements

    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        _reinforcement_order = self.get_strategy_order_for_reinforcements()
        _strategy_reinforcements = self.get_strategy_reinforcements(
            strategy_input.strategy_locations, _reinforcement_order
        )
        OrderStrategyBuffering.with_strategy(
            _reinforcement_order, strategy_input.reinforcement_min_buffer
        ).apply(_strategy_reinforcements)
        OrderStrategyClustering.with_strategy(
            _reinforcement_order, strategy_input.reinforcement_min_length
        ).apply(_strategy_reinforcements)
        return _strategy_reinforcements
