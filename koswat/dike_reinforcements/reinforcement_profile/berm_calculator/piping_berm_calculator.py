from dataclasses import dataclass

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_base import (
    BermCalculatorBase,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_protocol import (
    BermCalculatorProtocol,
)


@dataclass
class PipingBermCalculator(BermCalculatorBase, BermCalculatorProtocol):
    """
    Calculator for the berm width, height and slope for the polderside of the dike
    in case of piping.
    """

    dikebase_piping_new: float

    def calculate(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
    ) -> tuple[float, float, float]:
        _polderside_berm_width = self.dikebase_piping_new - max(
            self.dikebase_height_new, self.dikebase_stability_new
        )
        _polderside_slope = self._calculate_new_polderside_slope(base_data, None)
        # extend existing berm?
        reinforced_data.polderside_berm_width = _polderside_berm_width
        if base_data.polderside_berm_width > 0 and self.dikebase_piping_old > max(
            self.dikebase_height_new, self.dikebase_stability_new
        ):
            _polderside_berm_height = self._calculate_new_polderside_berm_height_piping(
                base_data,
                reinforced_data,
                True,
            )
        else:
            _polderside_berm_height = self._calculate_new_polderside_berm_height_piping(
                base_data,
                reinforced_data,
                False,
            )

        return (_polderside_berm_width, _polderside_berm_height, _polderside_slope)
