from dataclasses import dataclass

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_base import (
    BermCalculatorBase,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_protocol import (
    BermCalculatorProtocol,
)


@dataclass
class StabilityBermCalculator(BermCalculatorBase, BermCalculatorProtocol):
    """
    Calculator for the berm width, height and slope for the polderside of the dike
    in case of stability.
    """

    berm_factor_old: float

    def calculate(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
    ) -> tuple[float, float, float]:
        _polderside_berm_width = self.dikebase_stability_new - self.dikebase_height_new
        _polderside_berm_height = (
            self.berm_factor_old * self.dike_height_new
            + base_data.polderside_ground_level
        )
        _polderside_slope = base_data.polderside_slope

        return (_polderside_berm_width, _polderside_berm_height, _polderside_slope)
