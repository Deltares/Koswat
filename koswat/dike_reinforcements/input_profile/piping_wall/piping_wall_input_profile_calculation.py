from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_piping_settings import (
    KoswatPipingSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)


class PipingWallInputProfileCalculation(ReinforcementInputProfileCalculationProtocol):
    base_profile: KoswatProfileProtocol
    piping_settings: KoswatPipingSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_soil_binnen_berm_breedte(
        self,
        old_data: KoswatInputProfileBase,
        new_data: KoswatInputProfileBase,
        scenario: KoswatScenario,
    ) -> float:
        """
        Redundant code to reproduce the new berm width that would have been calculated by soil calculation
        """
        _c1 = scenario.buiten_talud + new_data.binnen_talud
        _c2 = old_data.kruin_hoogte - old_data.binnen_maaiveld + scenario.d_h
        _c3 = old_data.buiten_talud + old_data.binnen_talud
        _c4 = new_data.buiten_berm_breedte - old_data.buiten_berm_breedte
        _c5 = (
            _c3 * (old_data.kruin_hoogte - old_data.binnen_maaiveld)
            + old_data.kruin_breedte
            - _c4
        )
        _c6 = _c1 * _c2 + new_data.kruin_breedte - _c5
        _c7 = old_data.binnen_berm_breedte + scenario.d_p - _c6
        return max(_c7, 0)

    def _calculate_length_piping_wall(
        self,
        old_data: KoswatInputProfileBase,
        piping_settings: KoswatPipingSettings,
        soil_binnen_berm_breedte: float,
    ) -> float:
        if soil_binnen_berm_breedte == 0:
            return 0
        _length = (
            (soil_binnen_berm_breedte / 6)
            + (old_data.binnen_maaiveld - old_data.aquifer)
            + 1
        )
        _length = max(_length, piping_settings.min_lengte_kwelscherm)
        _length = min(_length, piping_settings.max_lengte_kwelscherm)

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
                +(Kruin_Hoogte_Oud-Binnen_Maaiveld_Oud)*Binnen_Talud_Oud)
                /(Kruin_Hoogte_Oud-Binnen_Maaiveld_Oud+dH))
        """
        _first_part = scenario.d_h * scenario.buiten_talud
        _second_part = scenario.kruin_breedte - base_data.kruin_breedte
        _third_parth = (
            base_data.kruin_hoogte - base_data.binnen_maaiveld
        ) * base_data.binnen_talud
        _dividend = base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h
        _right_side = (
            scenario.d_s - _first_part - _second_part + _third_parth
        ) / _dividend
        return max(base_data.binnen_talud, _right_side)

    def _calculate_new_input_profile(
        self,
        base_data: KoswatInputProfileProtocol,
        piping_settings: KoswatPipingSettings,
        scenario: KoswatScenario,
    ) -> PipingWallInputProfile:
        _new_data = PipingWallInputProfile()
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
        _soil_binnen_berm_breedte = self._calculate_soil_binnen_berm_breedte(
            base_data, _new_data, scenario
        )
        _new_data.length_piping_wall = self._calculate_length_piping_wall(
            base_data, piping_settings, _soil_binnen_berm_breedte
        )
        return _new_data

    def build(self) -> PipingWallInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data, self.piping_settings, self.scenario
        )
