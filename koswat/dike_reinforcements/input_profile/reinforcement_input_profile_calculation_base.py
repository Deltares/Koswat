from abc import ABC

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.configuration.settings.reinforcements.koswat_soil_settings import KoswatSoilSettings

class ReinforcementInputProfileCalculationBase(ABC):
    """
    Abstract class to provide common functions to child classes
    """
    def _calculate_soil_new_kruin_hoogte(self, base_data: KoswatInputProfileBase, scenario: KoswatScenario) -> float:
        return base_data.kruin_hoogte + scenario.d_h

    def _calculate_soil_new_buiten_berm_hoogte(self, base_data: KoswatInputProfileBase, scenario: KoswatScenario) -> float:
        if base_data.buiten_berm_hoogte > base_data.buiten_maaiveld:       
            return base_data.buiten_berm_hoogte + scenario.d_h
        return base_data.buiten_berm_hoogte
    
    def _calculate_soil_new_binnen_talud(self, base_data: KoswatInputProfileBase, scenario: KoswatScenario, dikebase_heigth_new: float, dikebase_stability_new: float) -> float:
        _operand = max(dikebase_heigth_new, dikebase_stability_new) - scenario.d_h * scenario.buiten_talud - scenario.kruin_breedte
        _dividend = base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h
        return _operand / _dividend
    
    def _calculate_soil_new_binnen_berm_hoogte_piping(self, old_data: KoswatInputProfileBase, new_data: KoswatInputProfileBase, scenario: KoswatScenario, soil_settings: KoswatSoilSettings, berm_extend_existing: bool) -> float:
        if berm_extend_existing:
            _old_berm_height = old_data.binnen_berm_hoogte - old_data.binnen_maaiveld
        else:
            _old_berm_height = 0
        _max = max(
            soil_settings.min_bermhoogte,
            _old_berm_height,
            new_data.binnen_berm_breedte * soil_settings.factor_toename_bermhoogte,
        )
        return (
            min(_max, soil_settings.max_bermhoogte_factor * (new_data.kruin_hoogte - new_data.binnen_maaiveld)) + new_data.binnen_maaiveld
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
