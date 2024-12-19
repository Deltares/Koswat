from dataclasses import dataclass

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_protocol import (
    BermCalculatorProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_result import (
    BermCalculatorResult,
)


@dataclass
class KeepBermCalculator(BermCalculatorProtocol):
    """
    Calculator for keeping the berm width for the polderside of the dike
    but calculating the height and slope.
    """

    scenario: KoswatScenario
    dikebase_piping_old: float
    dikebase_piping_new: float
    dike_height_new: float

    def calculate(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
    ) -> BermCalculatorResult:
        _polderside_berm_width = (
            base_data.polderside_berm_width
        )  # maintain current berm polderside
        _polderside_berm_height = self._calculate_new_keep_polderside_berm_height(
            base_data
        )
        _polderside_slope = self._calculate_new_keep_polderside_slope(base_data)

        return BermCalculatorResult(
            berm_width=_polderside_berm_width,
            berm_height=_polderside_berm_height,
            slope=_polderside_slope,
        )

    def _calculate_new_keep_polderside_berm_height(
        self, base_data: KoswatInputProfileProtocol
    ) -> float:
        _dike_height_old = base_data.crest_height - base_data.polderside_ground_level
        _berm_height_old = (
            base_data.polderside_berm_height - base_data.polderside_ground_level
        )
        _berm_factor_old = _berm_height_old / _dike_height_old

        return base_data.polderside_berm_height + _berm_factor_old * self.scenario.d_h

    def _calculate_new_keep_polderside_slope(
        self, base_data: KoswatInputProfileProtocol
    ) -> float:
        _operand = (
            base_data.crest_height - base_data.polderside_ground_level
        ) * base_data.polderside_slope
        _dividend = (
            base_data.crest_height
            - base_data.polderside_ground_level
            + self.scenario.d_h
        )
        return _operand / _dividend
