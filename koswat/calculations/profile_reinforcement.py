from koswat.calculations.profile_calculation_protocol import ProfileCalculationProtocol
from koswat.dike.koswat_profile.koswat_input_profile import KoswatInputProfile
from koswat.dike.koswat_profile.koswat_profile import KoswatProfileBase
from koswat.dike.koswat_profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario


class ProfileReinforcement(KoswatProfileBase):
    def __str__(self) -> str:
        return "Grondmaatregel profiel"


class ProfileReinforcementCalculation(ProfileCalculationProtocol):
    def _calculate_new_binnen_talud(
        self, old_data: KoswatInputProfile, scenario: KoswatScenario
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
        _second_part = scenario.kruin_breedte - old_data.kruin_breedte
        _third_parth = old_data.kruin_hoogte * old_data.binnen_talud
        _dividend = old_data.kruin_hoogte + scenario.d_h
        _right_side = (
            scenario.d_s - _first_part - _second_part + _third_parth
        ) / _dividend
        return max(old_data.binnen_talud, _right_side)

    def _calculate_new_binnen_berm_hoogte(
        self,
        old_data: KoswatInputProfile,
        new_data: KoswatInputProfile,
        scenario: KoswatScenario,
    ) -> float:
        if new_data.binnen_berm_breedte > 0:
            _max = max(
                0.5, old_data.binnen_berm_hoogte, new_data.binnen_berm_breedte * 0.05
            )
            return min(_max, 0.4 * (old_data.kruin_hoogte + scenario.d_h))
        return 0

    def _calculate_new_binnen_berm_breedte(
        self,
        old_data: KoswatInputProfile,
        new_data: KoswatInputProfile,
        scenario: KoswatScenario,
    ) -> float:
        _c1 = scenario.buiten_talud + new_data.binnen_talud
        _c2 = old_data.kruin_hoogte + scenario.d_h
        _c3 = old_data.buiten_talud + old_data.binnen_talud
        _c4 = new_data.buiten_berm_breedte - old_data.buiten_berm_breedte
        _c5 = _c3 * old_data.kruin_hoogte + old_data.kruin_breedte - _c4
        _c6 = _c1 * _c2 + new_data.kruin_breedte - _c5
        _c7 = old_data.binnen_berm_breedte + scenario.d_p - _c6
        return max(_c7, 0)

    def _calculate_new_kruin_hoogte(
        self, old_data: KoswatInputProfile, scenario: KoswatScenario
    ) -> float:
        return old_data.kruin_hoogte + scenario.d_h

    def _calculate_new_input_profile(
        self, old_data: KoswatInputProfile, scenario: KoswatScenario
    ) -> KoswatInputProfile:
        _new_data = KoswatInputProfile()
        _new_data.buiten_maaiveld = old_data.buiten_maaiveld
        _new_data.buiten_talud = scenario.buiten_talud
        _new_data.buiten_berm_hoogte = old_data.buiten_berm_hoogte
        _new_data.buiten_berm_breedte = old_data.buiten_berm_breedte
        _new_data.kruin_hoogte = self._calculate_new_kruin_hoogte(old_data, scenario)
        _new_data.kruin_breedte = scenario.kruin_breedte
        _new_data.binnen_talud = self._calculate_new_binnen_talud(old_data, scenario)
        _new_data.binnen_berm_breedte = self._calculate_new_binnen_berm_breedte(
            old_data, _new_data, scenario
        )
        _new_data.binnen_berm_hoogte = self._calculate_new_binnen_berm_hoogte(
            old_data, _new_data, scenario
        )
        _new_data.binnen_maaiveld = old_data.binnen_maaiveld
        return _new_data

    def calculate_new_profile(
        self, profile: KoswatProfileBase, scenario: KoswatScenario
    ) -> KoswatProfileBase:
        _new_data = self._calculate_new_input_profile(profile.input_data, scenario)
        _data_layers = profile.layers.as_data_dict()
        _builder_dict = dict(
            input_profile_data=_new_data.__dict__,
            layers_data=_data_layers,
            p4_x_coordinate=scenario.d_h * scenario.buiten_talud,
        )
        return KoswatProfileBuilder.with_data(_builder_dict).build(ProfileReinforcement)
