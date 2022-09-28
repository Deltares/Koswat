from koswat.calculations.calculation_protocol import CalculationProtocol
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_profile import KoswatProfile


class ProfileReinforcement(CalculationProtocol):
    def calculate_new_talud(
        self, old_data: KoswatInputProfile, scenario: KoswatScenario
    ) -> float:
        _operand = (
            scenario.d_s
            - (scenario.d_h * scenario.buiten_talud)
            - (scenario.kruin_breedte - old_data.kruin_breedte)
            + old_data.kruin_hoogte * old_data.binnen_talud
        )
        _dividend = old_data.kruin_hoogte + scenario.d_h
        return max(old_data.binnen_talud, _operand / _dividend)

    def calculate_new_berm_hoogte(
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

    def calculate_new_berm_breedte(
        self,
        old_data: KoswatInputProfile,
        new_data: KoswatInputProfile,
        scenario: KoswatScenario,
    ) -> float:
        _left_side = (
            old_data.binnen_berm_breedte
            + scenario.d_p
            - (scenario.buiten_talud + new_data.binnen_talud)
            * (old_data.kruin_hoogte + scenario.d_h)
            + scenario.kruin_breedte
            - (
                (old_data.buiten_talud + old_data.binnen_talud) * old_data.kruin_hoogte
                + old_data.kruin_breedte
                - (new_data.buiten_berm_breedte - old_data.buiten_berm_breedte)
            )
        )
        return max(_left_side, 0)

    def calculate_new_kruin_hoogte(
        self, old_data: KoswatInputProfile, scenario: KoswatScenario
    ) -> float:
        return old_data.buiten_berm_hoogte + scenario.d_h

    def _calculate_new_input_profile(
        self, old_data: KoswatInputProfile, scenario: KoswatScenario
    ) -> KoswatInputProfile:
        _new_data = KoswatInputProfile()
        _new_data.buiten_maaiveld = old_data.buiten_maaiveld
        _new_data.buiten_talud = scenario.buiten_talud
        _new_data.buiten_berm_hoogte = old_data.buiten_berm_hoogte
        _new_data.buiten_berm_breedte = old_data.buiten_berm_breedte
        _new_data.kruin_hoogte = self.calculate_new_kruin_hoogte(old_data, scenario)
        _new_data.kruin_breedte = scenario.kruin_breedte
        _new_data.binnen_talud = self.calculate_new_talud(old_data, scenario)
        _new_data.binnen_berm_breedte = self.calculate_new_berm_breedte(
            old_data, _new_data, scenario
        )
        _new_data.binnen_berm_hoogte = self.calculate_new_berm_hoogte(
            old_data, _new_data, scenario
        )
        _new_data.binnen_maaiveld = old_data.binnen_maaiveld
        return old_data

    def calculate_new_geometry(
        self, profile: KoswatProfile, scenario: KoswatScenario
    ) -> KoswatProfile:
        _new_data = self._calculate_new_input_profile(profile.input_data, scenario)
        return KoswatProfile.from_koswat_input_profile(_new_data)
