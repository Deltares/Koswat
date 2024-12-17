from dataclasses import dataclass

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_base import (
    BermCalculatorBase,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_protocol import (
    BermCalculatorProtocol,
)


@dataclass
class NoBermCalculator(BermCalculatorBase, BermCalculatorProtocol):
    def calculate(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
    ) -> tuple[float, float, float]:
        _polderside_berm_width = 0
        _polderside_berm_height = base_data.polderside_ground_level
        _polderside_slope = self._calculate_new_polderside_slope(base_data)

        return (_polderside_berm_width, _polderside_berm_height, _polderside_slope)
