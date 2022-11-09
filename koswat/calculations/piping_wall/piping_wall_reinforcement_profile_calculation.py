from email.mime import base

from koswat.calculations.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.calculations.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario


class PipingWallReinforcementProfileCalculation(
    ReinforcementInputProfileCalculationProtocol
):
    base_profile: KoswatProfileProtocol
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_length_piping_wall(
        self, new_data: KoswatInputProfileProtocol
    ) -> float:
        return (new_data.binnen_berm_breedte / 6) + 1.5

    def _calculate_new_kruin_hoogte(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.kruin_hoogte + scenario.d_h

    def _calculate_new_binnen_talud(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        """
        MAX(
            Binnen_Talud_Oud,
            (
                dS
                -dH*Buiten_Talud_Nieuw
                -(Kruin_Breedte_Nieuw-Kruin_Breedte_Oud)
                +Kruin_Hoogte_Oud*Binnen_Talud_Oud)
                /(Kruin_Hoogte_Oud+dH))
        """
        _first_part = scenario.d_h * scenario.buiten_talud
        _second_part = scenario.kruin_breedte - base_data.kruin_breedte
        _third_parth = base_data.kruin_hoogte * base_data.binnen_talud
        _dividend = base_data.kruin_hoogte + scenario.d_h
        _right_side = (
            scenario.d_s - _first_part - _second_part + _third_parth
        ) / _dividend
        return max(base_data.binnen_talud, _right_side)

    def _calculate_new_input_profile(
        self, base_data: KoswatInputProfileProtocol, scenario: KoswatScenario
    ) -> PipingWallInputProfile:
        _new_data = PipingWallInputProfile()
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.buiten_talud = scenario.buiten_talud
        _new_data.buiten_berm_hoogte = base_data.buiten_berm_hoogte
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte
        _new_data.kruin_hoogte = self._calculate_new_kruin_hoogte(base_data, scenario)
        _new_data.kruin_breedte = scenario.kruin_breedte
        _new_data.binnen_talud = self._calculate_new_binnen_talud(base_data, scenario)
        _new_data.binnen_berm_hoogte = 0
        _new_data.binnen_berm_breedte = 0
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        _new_data.length_piping_wall = self._calculate_length_piping_wall(_new_data)
        return _new_data

    def build(self) -> PipingWallReinforcementProfile:
        _new_data = self._calculate_new_input_profile(
            self.base_profile.input_data, self.scenario
        )
        _data_layers = self.base_profile.layers_wrapper.as_data_dict()
        _builder_dict = dict(
            input_profile_data=_new_data.__dict__,
            layers_data=_data_layers,
            p4_x_coordinate=self.scenario.d_h * self.scenario.buiten_talud,
            profile_type=PipingWallReinforcementProfile,
        )
        return KoswatProfileBuilder.with_data(_builder_dict).build()
