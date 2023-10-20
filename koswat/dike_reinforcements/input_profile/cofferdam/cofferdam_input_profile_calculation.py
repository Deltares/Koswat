from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class CofferdamInputProfileCalculation(ReinforcementInputProfileCalculationProtocol):
    base_profile: KoswatProfileProtocol
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_new_kruin_hoogte(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.kruin_hoogte + scenario.d_h

    def _calculate_new_binnen_talud(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        """
        ( Kruin_Breedte_Oud
            + (Kruin_Hoogte_Oud-Binnen_Maaiveld_Oud)
                *Binnen_Talud_Oud-Kruin_Breedte_Nieuw)
        /(Kruin_Hoogte_Oud+dH)
        """
        _mid_operand = base_data.binnen_talud * (
            base_data.kruin_hoogte - base_data.binnen_maaiveld
        )
        _operand = base_data.kruin_breedte + _mid_operand - scenario.kruin_breedte
        _dividend = base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h
        return _operand / _dividend

    def _calculate_new_buiten_talud(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        """
        Kruin_Hoogte_Oud*Buiten_Talud_Oud
        /(Kruin_Hoogte_Oud+dH)
        """
        _operand = (
            base_data.kruin_hoogte - base_data.buiten_maaiveld
        ) * base_data.buiten_talud
        _dividend = base_data.kruin_hoogte - base_data.buiten_maaiveld + scenario.d_h
        return _operand / _dividend

    def _calculate_new_length_coffer_dam(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return (
            (base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h) - 1 + 10
        )

    def _calculate_new_input_profile(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> CofferDamInputProfile:
        _new_data = CofferDamInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.buiten_talud = self._calculate_new_buiten_talud(base_data, scenario)
        _new_data.buiten_berm_hoogte = base_data.buiten_berm_hoogte
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte
        _new_data.kruin_hoogte = self._calculate_new_kruin_hoogte(base_data, scenario)
        _new_data.kruin_breedte = scenario.kruin_breedte
        _new_data.binnen_talud = self._calculate_new_binnen_talud(base_data, scenario)
        _new_data.binnen_berm_breedte = 0
        _new_data.binnen_berm_hoogte = base_data.binnen_maaiveld
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        _new_data.length_coffer_dam = self._calculate_new_length_coffer_dam(
            base_data, scenario
        )
        return _new_data

    def build(self) -> CofferDamInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data, self.scenario
        )
