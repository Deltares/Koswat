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
        _first_part = scenario.d_h * scenario.buiten_talud
        _second_part = scenario.kruin_breedte - base_data.crest_width
        _third_parth = (
            base_data.crest_height - base_data.polderside_ground_level
        ) * base_data.polderside_slope
        _dividend = (
            base_data.crest_height - base_data.polderside_ground_level + scenario.d_h
        )
        _right_side = (
            scenario.d_s - _first_part - _second_part + _third_parth
        ) / _dividend
        return max(base_data.polderside_slope, _right_side)

    def _calculate_new_binnen_berm_hoogte(
        self,
        old_data: KoswatInputProfileBase,
        new_data: KoswatInputProfileBase,
        scenario: KoswatScenario,
    ) -> float:
        if new_data.polderside_berm_width > 0:
            _max = max(
                0.5,
                (old_data.polderside_berm_height - old_data.polderside_ground_level),
                new_data.polderside_berm_width * 0.05,
            )
            return (
                min(
                    _max,
                    0.4
                    * (
                        (old_data.crest_height - old_data.polderside_ground_level)
                        + scenario.d_h
                    ),
                )
                + old_data.polderside_ground_level
            )
        return old_data.polderside_ground_level

    def _calculate_new_kruin_hoogte(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.crest_height + scenario.d_h

    def _calculate_new_input_profile(
        self,
        base_data: KoswatInputProfileBase,
        soil_settings: KoswatSoilSettings,
        scenario: KoswatScenario,
    ) -> KoswatInputProfileBase:
        _new_data = SoilInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.waterside_ground_level = base_data.waterside_ground_level
        _new_data.waterside_slope = scenario.buiten_talud
        _new_data.waterside_berm_height = base_data.waterside_berm_height
        _new_data.waterside_berm_width = base_data.waterside_berm_width
        _new_data.crest_width = scenario.kruin_breedte
        _new_data.crest_height = self._calculate_new_kruin_hoogte(base_data, scenario)
        _new_data.polderside_ground_level = base_data.polderside_ground_level
        _new_data.polderside_slope = self._calculate_new_binnen_talud(
            base_data, scenario
        )
        _new_data.polderside_berm_width = self._calculate_soil_binnen_berm_breedte(
            base_data, _new_data, scenario
        )
        _new_data.polderside_berm_height = self._calculate_new_binnen_berm_hoogte(
            base_data, _new_data, scenario
        )
        _new_data.ground_price_builtup = base_data.ground_price_builtup
        _new_data.ground_price_unbuilt = base_data.ground_price_unbuilt
        _new_data.factor_settlement = base_data.factor_settlement
        _new_data.pleistocene = base_data.pleistocene
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
