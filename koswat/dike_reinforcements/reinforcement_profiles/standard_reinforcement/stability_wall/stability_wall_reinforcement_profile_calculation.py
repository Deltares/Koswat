from koswat.dike_reinforcements.reinforcement_profiles.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.reinforcement_profiles.standard_reinforcement.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class StabilityWallReinforcementProfileCalculation(
    ReinforcementInputProfileCalculationProtocol
):
    base_profile: KoswatProfileProtocol
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_length_stability_wall(
        self, base_data: KoswatInputProfileProtocol, scenario: KoswatScenario
    ) -> float:
        return (
            (base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h) - 1 + 10
        )

    def _calculate_new_kruin_hoogte(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.kruin_hoogte + scenario.d_h

    def _calculate_new_binnen_talud(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        """
        MAX(
            2,
            ( Kruin_Breedte_Oud
            +
            (Kruin_Hoogte_Oud-Binnen_Maaiveld_Oud)
            *Binnen_Talud_Oud
            -dH*Buiten_Talud_Nieuw
            -Kruin_Breedte_Nieuw)
            /(Kruin_Hoogte_Oud+dH))

        """
        _first_part = (
            base_data.kruin_hoogte - base_data.binnen_maaiveld
        ) * base_data.binnen_talud
        _second_part = scenario.d_h * scenario.buiten_talud
        _operand = (
            base_data.kruin_breedte
            + _first_part
            - _second_part
            - scenario.kruin_breedte
        )
        _dividend = base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h
        _right_side = _operand / _dividend
        return max(2, _right_side)

    def _calculate_new_input_profile(
        self, base_data: KoswatInputProfileProtocol, scenario: KoswatScenario
    ) -> StabilityWallInputProfile:
        _new_data = StabilityWallInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.buiten_talud = scenario.buiten_talud
        _new_data.buiten_berm_hoogte = base_data.buiten_berm_hoogte
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte
        _new_data.kruin_hoogte = self._calculate_new_kruin_hoogte(base_data, scenario)
        _new_data.kruin_breedte = scenario.kruin_breedte
        _new_data.binnen_talud = self._calculate_new_binnen_talud(base_data, scenario)
        _new_data.binnen_berm_hoogte = base_data.binnen_maaiveld
        _new_data.binnen_berm_breedte = 0
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        _new_data.length_stability_wall = self._calculate_length_stability_wall(
            base_data, scenario
        )
        return _new_data

    def build(self) -> StabilityWallInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data, self.scenario
        )
