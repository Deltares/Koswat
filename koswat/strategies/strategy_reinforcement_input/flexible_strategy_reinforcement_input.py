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

from dataclasses import dataclass
from .strategy_reinforcement_input_base import (
    StrategyReinforcementInputBase,
)


@dataclass(kw_only=True)
class FlexibleStrategyReinforcementInput(StrategyReinforcementInputBase):
    """
    A `FlexibleStrategyReinforcementInput` is a `StrategyReinforcementInput` that can be
    filtered out by other reinforcements based on costs and ground level surface.
    This is useful for cases where certain reinforcements are optional or have
    specific constraints that allow them to be excluded.
    """

    pass
