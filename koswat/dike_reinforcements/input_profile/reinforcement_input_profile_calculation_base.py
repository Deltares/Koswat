from abc import ABC

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class ReinforcementInputProfileCalculationBase(ABC):
    """
    Abstract class to provide common functions to child classes
    """

    def _calculate_soil_binnen_berm_breedte(
        self,
        old_data: KoswatInputProfileBase,
        new_data: KoswatInputProfileBase,
        scenario: KoswatScenario,
    ) -> float:
        _dikebase_old = (
            (old_data.kruin_hoogte - old_data.buiten_maaiveld) * old_data.buiten_talud
            + old_data.buiten_berm_breedte
            + old_data.kruin_breedte
            + old_data.binnen_berm_breedte
            + (old_data.kruin_hoogte - old_data.binnen_maaiveld) * old_data.binnen_talud
        )
        _dikebase_new = (
            (new_data.kruin_hoogte - new_data.buiten_maaiveld) * new_data.buiten_talud
            + new_data.buiten_berm_breedte
            + new_data.kruin_breedte
            + (new_data.kruin_hoogte - new_data.binnen_maaiveld) * new_data.binnen_talud
        )
        _berm = scenario.d_p - (_dikebase_new - _dikebase_old)
        return max(_berm, 0)
