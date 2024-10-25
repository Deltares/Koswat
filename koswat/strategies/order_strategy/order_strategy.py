from __future__ import annotations

import math
from itertools import pairwise

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
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)


class OrderStrategy(StrategyProtocol):
    @staticmethod
    def get_default_order_for_reinforcements() -> list[
        type[ReinforcementProfileProtocol]
    ]:
        """
        Give the default order for reinforcements types,
        assuming they are sorted from cheapest to most expensive
        and least to most restrictive.

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
        strategy_input: StrategyInput,
    ) -> list[type[ReinforcementProfileProtocol]]:
        """
        Give the ordered reinforcement types for this strategy, from cheapest to most expensive,
        possibly removing reinforcement types that are more expensive and more restrictive than others.
        Cofferdam should always be the last reinforcement type.

        Returns:
            list[type[ReinforcementProfileProtocol]]: list of reinforcement types
        """

        def split_reinforcements() -> tuple[
            list[StrategyReinforcementTypeCosts], list[StrategyReinforcementTypeCosts]
        ]:
            _cofferdam = next(
                obj
                for obj in strategy_input.strategy_reinforcement_type_costs
                if obj.reinforcement_type == CofferdamReinforcementProfile
            )
            return (
                [
                    obj
                    for obj in strategy_input.strategy_reinforcement_type_costs
                    if obj.reinforcement_type != CofferdamReinforcementProfile
                ],
                [_cofferdam],
            )

        # Split in a list to be sorted (cheap to expensive) and a list to be put last (Cofferdam for now)
        _unsorted, _last = split_reinforcements()
        _sorted = sorted(
            _unsorted, key=lambda x: (x.base_costs, x.ground_level_surface)
        )

        def check_reinforcement(
            pair: tuple[StrategyReinforcementTypeCosts, StrategyReinforcementTypeCosts],
        ) -> StrategyReinforcementTypeCosts | None:
            # Only keep the more expensive reinforcement if it is more restrictive
            if pair[1].ground_level_surface < pair[0].ground_level_surface:
                return pair[1]
            return None

        # Check if the current (more expensive) reinforcement is more restrictive than the previous
        # (the first needs to be prepended as it is always kept)
        _sorted_pairs = pairwise(_sorted)
        _kept = [_sorted[0]] + list(map(check_reinforcement, _sorted_pairs))

        return [x.reinforcement_type for x in _kept if x] + [
            x.reinforcement_type for x in _last
        ]

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
        _reinforcement_order = self.get_strategy_order_for_reinforcements(
            strategy_input
        )
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
