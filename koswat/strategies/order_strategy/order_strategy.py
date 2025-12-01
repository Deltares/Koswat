"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from itertools import product

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
from koswat.strategies.strategy_output import StrategyOutput
from koswat.strategies.strategy_protocol import StrategyProtocol
from koswat.strategies.strategy_reinforcement_input import StrategyReinforcementInput
from koswat.strategies.strategy_step.strategy_step_enum import StrategyStepEnum


class OrderStrategy(StrategyProtocol):
    reinforcement_order: list[type[ReinforcementProfileProtocol]]

    @staticmethod
    def get_default_order_for_reinforcements() -> (
        list[type[ReinforcementProfileProtocol]]
    ):
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
        Inactive reinforcements are ignored.
        Cofferdam should always be the last reinforcement type.

        Input:
            strategy_reinforcements (list[StrategyReinforcementInput]): list of reinforcement types with costs and surface

        Returns:
            list[type[ReinforcementProfileProtocol]]: list of reinforcement types
        """
        if not strategy_reinforcements:
            return []

        def split_reinforcements() -> (
            tuple[list[StrategyReinforcementInput], list[StrategyReinforcementInput]]
        ):
            _last, _other = [], []
            for obj in strategy_reinforcements:
                if not obj:
                    continue
                if obj.reinforcement_type == CofferdamReinforcementProfile:
                    _last.append(obj)
                    continue
                if not obj.active:
                    continue
                else:
                    _other.append(obj)

            return (_other, _last)

        # Split in a list to be sorted (least to most restrictive) and a list to be put last (Cofferdam for now)
        _unsorted, _last = split_reinforcements()
        _sorted = sorted(
            _unsorted,
            key=lambda x: (x.ground_level_surface, x.base_costs_with_surtax),
            reverse=True,
        )

        # Remove the reinforcements that are more expensive and less or equally restrictive than 1 of the others
        def remove_reinforcement(
            pair: tuple[StrategyReinforcementInput, StrategyReinforcementInput],
        ) -> bool:
            return (
                pair[0].base_costs_with_surtax > pair[1].base_costs_with_surtax
                and pair[0].ground_level_surface >= pair[1].ground_level_surface
            )

        for _pair in product(_sorted, _sorted + _last):
            if remove_reinforcement(_pair) and _pair[0] in _sorted:
                _sorted.remove(_pair[0])

        return [x.reinforcement_type for x in _sorted + _last]

    @staticmethod
    def get_strategy_reinforcements(
        strategy_locations: list[StrategyLocationInput],
        selection_order: list[type[ReinforcementProfileProtocol]],
    ) -> list[StrategyLocationReinforcement]:
        """
        Gets the strategy representation of the locations with their available measures
        ordered filtered and order by the provided `selection_order`. It also sets
        their initial state.

        Args:
            strategy_locations (list[StrategyLocationInput]): Locations to map into reinforcement locations.
            selection_order (list[type[ReinforcementProfileProtocol]]): Priority order to assign a reinforcement.

        Returns:
            list[StrategyLocationReinforcement]: Mapped location reinforcements.
        """
        _strategy_reinforcements = []
        for _strategy_location in strategy_locations:
            # Create the strategy representation.
            _slr = StrategyLocationReinforcement(
                location=_strategy_location.point_surrounding,
                available_measures=_strategy_location.available_measures,
                filtered_measures=list(
                    filter(
                        lambda x: x in _strategy_location.available_measures,
                        selection_order,
                    )
                ),
                strategy_location_input=_strategy_location,
            )

            # Manually set the current selected measure if none available.
            if not any(_slr.available_measures):
                # TODO: Unclear why tests fail when setting this measure
                # as the only available measure.
                _slr.set_selected_measure(selection_order[-1], StrategyStepEnum.ORDERED)

            _strategy_reinforcements.append(_slr)
        return _strategy_reinforcements

    def apply_strategy(self, strategy_input: StrategyInput) -> StrategyOutput:
        self.reinforcement_order = self.get_strategy_order_for_reinforcements(
            strategy_input.strategy_reinforcements
        )
        _strategy_reinforcements = self.get_strategy_reinforcements(
            strategy_input.strategy_locations, self.reinforcement_order
        )
        OrderStrategyBuffering(
            reinforcement_order=self.reinforcement_order,
            reinforcement_min_buffer=strategy_input.reinforcement_min_buffer,
        ).apply(_strategy_reinforcements)
        OrderStrategyClustering(
            reinforcement_order=self.reinforcement_order,
            reinforcement_min_length=strategy_input.reinforcement_min_length,
        ).apply(_strategy_reinforcements)
        return StrategyOutput(
            location_reinforcements=_strategy_reinforcements,
            reinforcement_order=self.reinforcement_order,
        )
