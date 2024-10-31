from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile import (
    SoilInputProfile,
)


class SoilInputProfileCalculation(
    ReinforcementInputProfileCalculationBase,
    ReinforcementInputProfileCalculationProtocol,
):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
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
        _first_part = scenario.d_h * scenario.waterside_slope
        _second_part = scenario.crest_width - base_data.kruin_breedte
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

    def _calculate_new_kruin_hoogte(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.kruin_hoogte + scenario.d_h

    def _calculate_new_input_profile(
        self,
        base_data: KoswatInputProfileBase,
        soil_settings: KoswatSoilSettings,
        scenario: KoswatScenario,
    ) -> KoswatInputProfileBase:
        _new_data = SoilInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.buiten_talud = scenario.waterside_slope
        _new_data.buiten_berm_hoogte = base_data.buiten_berm_hoogte
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte
        _new_data.kruin_breedte = scenario.crest_width
        _new_data.kruin_hoogte = self._calculate_new_kruin_hoogte(base_data, scenario)
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        _new_data.binnen_talud = self._calculate_new_binnen_talud(base_data, scenario)
        _new_data.binnen_berm_breedte = self._calculate_soil_binnen_berm_breedte(
            base_data, _new_data, scenario
        )
        _new_data.binnen_berm_hoogte = self._calculate_new_binnen_berm_hoogte(
            base_data, _new_data, scenario
        )
        _new_data.grondprijs_bebouwd = base_data.grondprijs_bebouwd
        _new_data.grondprijs_onbebouwd = base_data.grondprijs_onbebouwd
        _new_data.factor_zetting = base_data.factor_zetting
        _new_data.pleistoceen = base_data.pleistoceen
        _new_data.aquifer = base_data.aquifer
        _new_data.soil_surtax_factor = soil_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = None
        _new_data.land_purchase_surtax_factor = (
            soil_settings.land_purchase_surtax_factor
        )
        return _new_data

    def build(self) -> SoilInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data,
            self.reinforcement_settings.soil_settings,
            self.scenario,
        )
