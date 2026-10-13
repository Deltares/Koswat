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

import logging

from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_reinforcement_input.strategy_reinforcement_input_protocol import (
    StrategyReinforcementInputProtocol,
)
from koswat.strategies.strategy_reinforcement_filter_criteria_protocol import (
    StrategyReinforcementFilterCriteriaProtocol,
)
from koswat.strategies.strategy_reinforcement_widths import StrategyReinforcementWidths


class StrategyReinforcementWidthsFilterCriteria(
    StrategyReinforcementFilterCriteriaProtocol
):
    """
    This class is used to filter reinforcement profiles based on the width boundaries criteria.
    It checks if the reinforcement profiles polderside or waterside widths exceed the maximum allowed boundaries.
    """

    def __init__(
        self,
        strategy_input: StrategyInput,
    ):
        self._width_boundaries = StrategyReinforcementWidths(
            width_polderside=strategy_input.reinforcement_max_width_polderside,
            width_waterside=strategy_input.reinforcement_max_width_waterside,
        )

    def criteria_met_by(
        self, strategy_reinforcement: StrategyReinforcementInputProtocol
    ) -> bool:
        if strategy_reinforcement.is_within_boundaries(self._width_boundaries):
            return True
        logging.warning(
            "Reinforcement %s exceeds the maximum allowed width extension. Skipping.",
            strategy_reinforcement.reinforcement_type.output_name,
        )
        return False
