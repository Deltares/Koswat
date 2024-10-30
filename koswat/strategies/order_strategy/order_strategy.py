from __future__ import annotations

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
from koswat.strategies.strategy_reinforcement_input import StrategyReinforcementInput


class OrderStrategy(StrategyProtocol):
    reinforcement_order: list[type[ReinforcementProfileProtocol]]

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
        strategy_reinforcements: list[StrategyReinforcementInput],
    ) -> list[type[ReinforcementProfileProtocol]]:
        """
        Give the ordered reinforcement types for this strategy, from cheapest to most expensive,
        possibly removing reinforcement types that are more expensive and more restrictive than others.
        Cofferdam should always be the last reinforcement type.

        Input:
            strategy_reinforcements (list[StrategyReinforcementInput]): list of reinforcement types with costs and surface

        Returns:
            list[type[ReinforcementProfileProtocol]]: list of reinforcement types
        """
        if not strategy_reinforcements:
            return []

        def split_reinforcements() -> tuple[
            list[StrategyReinforcementInput], list[StrategyReinforcementInput]
        ]:
            _last, _other = [], []
            for obj in strategy_reinforcements:
                if not obj:
                    continue
                if obj.reinforcement_type == CofferdamReinforcementProfile:
                    _last.append(obj)
                else:
                    _other.append(obj)

            return (_other, _last)

        # Split in a list to be sorted (least to most restrictive) and a list to be put last (Cofferdam for now)
        _unsorted, _last = split_reinforcements()
        _sorted = sorted(
            _unsorted,
            key=lambda x: (x.ground_level_surface, x.base_costs),
            reverse=True,
        )

        def check_reinforcement(
            pair: tuple[StrategyReinforcementInput, StrategyReinforcementInput],
        ) -> StrategyReinforcementInput | None:
            # Only keep the less restrictive reinforcement if it is cheaper
            if (
                pair[0].ground_level_surface > pair[1].ground_level_surface
                and pair[0].base_costs < pair[1].base_costs
            ):
                return pair[0]
            return None

        # Check if the current (more expensive) reinforcement is more restrictive than the previous
        # (the last needs to be appended as it is always kept)
        _sorted_pairs = pairwise(_sorted + _last)
        _kept = (
            list(
                filter(lambda x: x is not None, map(check_reinforcement, _sorted_pairs))
            )
            + _last
        )

        return [x.reinforcement_type for x in _kept]

    @staticmethod
    def get_strategy_reinforcements(
        strategy_locations: list[StrategyLocationInput],
        selection_order: list[type[ReinforcementProfileProtocol]],
    ) -> list[StrategyLocationReinforcement]:
        _strategy_reinforcements = []
        _selection_order_set = set(selection_order)
        for _strategy_location in strategy_locations:
            # Get the available measures in the expected order!
            _available_measures = list(
                _selection_order_set.intersection(
                    set(_strategy_location.available_measures)
                )
            )

            # Create the strategy representation.
            _slr = StrategyLocationReinforcement(
                location=_strategy_location.point_surrounding,
                available_measures=_available_measures,
                strategy_location_input=_strategy_location,
            )

            # Manually set the current selected measure if none available.
            if not any(_slr.available_measures):
                # TODO: Unclear why tests fail when setting this measure
                # as the only available measure.
                _slr.current_selected_measure = selection_order[-1]

            _strategy_reinforcements.append(_slr)
        return _strategy_reinforcements

    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        self.reinforcement_order = self.get_strategy_order_for_reinforcements(
            strategy_input.strategy_reinforcements
        )
        _strategy_reinforcements = self.get_strategy_reinforcements(
            strategy_input.strategy_locations, self.reinforcement_order
        )
        OrderStrategyBuffering.with_strategy(
            self.reinforcement_order, strategy_input.reinforcement_min_buffer
        ).apply(_strategy_reinforcements)
        OrderStrategyClustering.with_strategy(
            self.reinforcement_order, strategy_input.reinforcement_min_length
        ).apply(_strategy_reinforcements)
        return _strategy_reinforcements
