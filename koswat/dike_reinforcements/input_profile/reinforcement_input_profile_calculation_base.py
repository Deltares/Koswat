from abc import ABC

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class ReinforcementInputProfileCalculationBase(ABC):
    """
    Abstract class to provide common functions to child classes
    """

    def _calculate_soil_polderside_berm_width(
        self,
        old_data: KoswatInputProfileBase,
        new_data: KoswatInputProfileBase,
        scenario: KoswatScenario,
    ) -> float:
        _dikebase_old = (
            (old_data.crest_height - old_data.waterside_ground_level)
            * old_data.waterside_slope
            + old_data.waterside_berm_width
            + old_data.crest_width
            + old_data.polderside_berm_width
            + (old_data.crest_height - old_data.polderside_ground_level)
            * old_data.polderside_slope
        )
        _dikebase_new = (
            (new_data.crest_height - new_data.waterside_ground_level)
            * new_data.waterside_slope
            + new_data.waterside_berm_width
            + new_data.crest_width
            + (new_data.crest_height - new_data.polderside_ground_level)
            * new_data.polderside_slope
        )
        _berm = scenario.d_p - (_dikebase_new - _dikebase_old)
        return max(_berm, 0)
