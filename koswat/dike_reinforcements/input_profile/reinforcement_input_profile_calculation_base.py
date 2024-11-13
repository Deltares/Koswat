from abc import ABC

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class ReinforcementInputProfileCalculationBase(ABC):
    """
    Abstract class to provide common functions to child classes
    """

    def _calculate_soil_new_crest_height(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.crest_height + scenario.d_h

    def _calculate_soil_new_waterside_berm_height(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        if base_data.waterside_berm_height > base_data.waterside_ground_level:
            return base_data.waterside_berm_height + scenario.d_h
        return base_data.waterside_berm_height

    def _calculate_soil_new_polderside_slope(
        self,
        base_data: KoswatInputProfileBase,
        scenario: KoswatScenario,
        dikebase_heigth_new: float,
        dikebase_stability_new: float,
    ) -> float:
        _operand = (
            max(dikebase_heigth_new, dikebase_stability_new)
            - scenario.d_h * scenario.waterside_slope
            - scenario.crest_width
        )
        _dividend = (
            base_data.crest_height - base_data.polderside_ground_level + scenario.d_h
        )
        return _operand / _dividend

    def _calculate_soil_new_polderside_berm_height_piping(
        self,
        old_data: KoswatInputProfileBase,
        new_data: KoswatInputProfileBase,
        scenario: KoswatScenario,
        soil_settings: KoswatSoilSettings,
        berm_extend_existing: bool,
    ) -> float:
        if berm_extend_existing:
            _old_berm_height = (
                old_data.polderside_berm_height - old_data.polderside_ground_level
            )
        else:
            _old_berm_height = 0
        _max = max(
            soil_settings.min_berm_height,
            _old_berm_height,
            new_data.polderside_berm_width * soil_settings.factor_increase_berm_height,
        )
        return (
            min(
                _max,
                soil_settings.max_berm_height_factor
                * (new_data.crest_height - new_data.polderside_ground_level),
            )
            + new_data.polderside_ground_level
        )


#    def _calculate_soil_binnen_berm_breedte(
#        self,
#        old_data: KoswatInputProfileBase,
#        new_data: KoswatInputProfileBase,
#        scenario: KoswatScenario,
#    ) -> float:
#        _dikebase_old = (
#            (old_data.kruin_hoogte - old_data.buiten_maaiveld) * old_data.buiten_talud
#            + old_data.buiten_berm_breedte
#            + old_data.kruin_breedte
#            + old_data.binnen_berm_breedte
#            + (old_data.kruin_hoogte - old_data.binnen_maaiveld) * old_data.binnen_talud
#        )
#        _dikebase_new = (
#            (new_data.kruin_hoogte - new_data.buiten_maaiveld) * new_data.buiten_talud
#            + new_data.buiten_berm_breedte
#            + new_data.kruin_breedte
#            + (new_data.kruin_hoogte - new_data.binnen_maaiveld) * new_data.binnen_talud
#        )
#        _berm = scenario.d_p - (_dikebase_new - _dikebase_old)
#        return max(_berm, 0)
