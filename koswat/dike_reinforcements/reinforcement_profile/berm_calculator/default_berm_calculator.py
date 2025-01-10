from dataclasses import dataclass

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_protocol import (
    BermCalculatorProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_result import (
    BermCalculatorResult,
)


@dataclass
class DefaultBermCalculator(BermCalculatorProtocol):
    """
    Calculator for the default berm width, height and slope for the polderside of the dike.
    """

    dikebase_piping_old: float
    dikebase_piping_new: float
    dike_height_new: float

    def calculate(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
    ) -> BermCalculatorResult:
        _polderside_berm_width = 0.0
        _polderside_berm_height = base_data.polderside_ground_level
        _polderside_slope = base_data.polderside_slope

        return BermCalculatorResult(
            berm_width=_polderside_berm_width,
            berm_height=_polderside_berm_height,
            slope=_polderside_slope,
        )
