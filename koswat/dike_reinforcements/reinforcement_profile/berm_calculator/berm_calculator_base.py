from abc import ABC
from dataclasses import dataclass

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator import (
    BermCalculatorProtocol,
)


@dataclass
class BermCalculatorBase(BermCalculatorProtocol, ABC):
    """
    Base class for calculating the berm height and slope of the polderside of the dike.
    """

    scenario: KoswatScenario
    reinforcement_settings: KoswatReinforcementSettings
    dikebase_piping_old: float
    dikebase_piping_new: float
    dikebase_height_new: float
    dikebase_stability_new: float
    dike_height_new: float

    def _calculate_new_polderside_slope(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforcement_type: InputProfileEnum,
    ) -> float:
        _dividend = (
            base_data.crest_height
            - base_data.polderside_ground_level
            + self.scenario.d_h
        )

        if reinforcement_type == InputProfileEnum.STABILITY_WALL:
            _operand = (
                self.dikebase_piping_old
                - self.scenario.d_h * self.scenario.waterside_slope
                - self.scenario.crest_width
            )
            return max(
                self.reinforcement_settings.stability_wall_settings.steepening_polderside_slope,
                _operand / _dividend,
            )

        _operand = (
            max(self.dikebase_height_new, self.dikebase_stability_new)
            - self.scenario.d_h * self.scenario.waterside_slope
            - self.scenario.crest_width
        )

        return _operand / _dividend

    def _calculate_new_polderside_berm_height_piping(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
        berm_extend_existing: bool,
    ) -> float:
        if berm_extend_existing:
            _old_berm_height = (
                base_data.polderside_berm_height - base_data.polderside_ground_level
            )
        else:
            _old_berm_height = 0.0
        _max = max(
            self.reinforcement_settings.soil_settings.min_berm_height,
            _old_berm_height,
            reinforced_data.polderside_berm_width
            * self.reinforcement_settings.soil_settings.factor_increase_berm_height,
        )
        return (
            min(
                _max,
                self.reinforcement_settings.soil_settings.max_berm_height_factor
                * (
                    reinforced_data.crest_height
                    - reinforced_data.polderside_ground_level
                ),
            )
            + reinforced_data.polderside_ground_level
        )
