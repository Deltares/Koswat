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
from typing import Optional

from koswat.dike_reinforcements.reinforcement_profile import (
    CofferdamReinforcementProfile,
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallCrestReinforcementProfile,
    StabilityWallToeReinforcementProfile,
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
            StabilityWallToeReinforcementProfile,
            StabilityWallCrestReinforcementProfile,
            CofferdamReinforcementProfile,
        ]

    def _split_reinforcements(
        self,
        reinforcements: list[StrategyReinforcementInput],
    ) -> tuple[
        list[StrategyReinforcementInput],
        Optional[StrategyReinforcementInput],
        StrategyReinforcementInput,
    ]:
        # All active items including Cofferdam, even if not active
        _unsorted = list(
            filter(
                lambda x: x.active
                or x.reinforcement_type == CofferdamReinforcementProfile,
                reinforcements,
            )
        )
        # SoilReinforcement, if active
        _first = next(
            (x for x in _unsorted if x.reinforcement_type == SoilReinforcementProfile),
            None,
        )
        # Cofferdam
        _last = next(
            (
                x
                for x in _unsorted
                if x.reinforcement_type == CofferdamReinforcementProfile
            )
        )

        return (_unsorted, _first, _last)

    def _merge_reinforcements(
        self,
        sorted: list[StrategyReinforcementInput],
        first: Optional[StrategyReinforcementInput],
        last: StrategyReinforcementInput,
    ) -> list[StrategyReinforcementInput]:
        # Remove first (if present) and last, to avoid duplicates.
        sorted.remove(first) if first in sorted else None
        sorted.remove(last) if last in sorted else None
        return [first] + sorted + [last] if first else sorted + [last]

    def get_strategy_order_for_reinforcements(
        self,
        strategy_reinforcements: list[StrategyReinforcementInput],
    ) -> list[type[ReinforcementProfileProtocol]]:
        """
        Give the ordered reinforcement types for this strategy, from cheapest to most expensive,
        possibly removing reinforcement types that are more expensive and more restrictive than others.
        Inactive reinforcements are ignored.
        If active, SoilReinforcement should be the first reinforcement type.
        Cofferdam should be the last reinforcement type.

        Input:
            strategy_reinforcements (list[StrategyReinforcementInput]): list of reinforcement types with costs and surface

        Returns:
            list[type[ReinforcementProfileProtocol]]: list of reinforcement types
        """
        if not strategy_reinforcements:
            return []

        # Order in a list to be sorted (least to most restrictive)
        # and find item to be put first and last.
        _unsorted, _first, _last = self._split_reinforcements(strategy_reinforcements)

        # Sort the reinforcements from least to most restrictive, and cheapest to most expensive.
        _sorted = sorted(
            _unsorted,
            key=lambda x: (x.ground_level_surface, x.base_costs_with_surtax),
            reverse=True,
        )

        # Remove the reinforcements that are more expensive and less or equally restrictive than 1 of the others.
        def remove_reinforcement(
            pair: tuple[StrategyReinforcementInput, StrategyReinforcementInput],
        ) -> bool:
            return (
                pair[0].base_costs_with_surtax > pair[1].base_costs_with_surtax
                and pair[0].ground_level_surface >= pair[1].ground_level_surface
            )

        for _pair in product(_sorted[:-1], _sorted):
            if remove_reinforcement(_pair) and _pair[0] in _sorted:
                _sorted.remove(_pair[0])

        return [
            x.reinforcement_type
            for x in self._merge_reinforcements(_sorted, _first, _last)
        ]

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
