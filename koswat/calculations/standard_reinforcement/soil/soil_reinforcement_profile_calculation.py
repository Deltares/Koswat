from koswat.calculations.protocols import ReinforcementInputProfileCalculationProtocol
from koswat.calculations.standard_reinforcement.soil.soil_input_profile import (
    SoilInputProfile,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class SoilReinforcementProfileCalculation(ReinforcementInputProfileCalculationProtocol):
    base_profile: KoswatProfileProtocol
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

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

    def _calculate_new_binnen_berm_hoogte(
        self,
        old_data: KoswatInputProfileBase,
        new_data: KoswatInputProfileBase,
        scenario: KoswatScenario,
    ) -> float:
        if new_data.binnen_berm_breedte > 0:
            _max = max(
                0.5,
                (old_data.binnen_berm_hoogte - old_data.binnen_maaiveld),
                new_data.binnen_berm_breedte * 0.05,
            )
            return (
                min(
                    _max,
                    0.4
                    * (
                        (old_data.kruin_hoogte - old_data.binnen_maaiveld)
                        + scenario.d_h
                    ),
                )
                + old_data.binnen_maaiveld
            )
        return old_data.binnen_maaiveld

    def _calculate_new_binnen_berm_breedte(
        self,
        old_data: KoswatInputProfileBase,
        new_data: KoswatInputProfileBase,
        scenario: KoswatScenario,
    ) -> float:
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

    def _calculate_new_kruin_hoogte(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.kruin_hoogte + scenario.d_h

    def _calculate_new_input_profile(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> KoswatInputProfileBase:
        _new_data = SoilInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.buiten_talud = scenario.buiten_talud
        _new_data.buiten_berm_hoogte = base_data.buiten_berm_hoogte
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte
        _new_data.kruin_hoogte = self._calculate_new_kruin_hoogte(base_data, scenario)
        _new_data.kruin_breedte = scenario.kruin_breedte
        _new_data.binnen_talud = self._calculate_new_binnen_talud(base_data, scenario)
        _new_data.binnen_berm_breedte = self._calculate_new_binnen_berm_breedte(
            base_data, _new_data, scenario
        )
        _new_data.binnen_berm_hoogte = self._calculate_new_binnen_berm_hoogte(
            base_data, _new_data, scenario
        )
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        return _new_data

    def build(self) -> SoilInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data, self.scenario
        )
