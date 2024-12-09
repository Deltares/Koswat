from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)


class CofferdamInputProfileCalculation(
    ReinforcementInputProfileCalculationBase,
    ReinforcementInputProfileCalculationProtocol,
):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_new_crest_height(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.crest_height + scenario.d_h

    def _calculate_new_polderside_slope(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        """
        ( Kruin_Breedte_Oud
            + (Kruin_Hoogte_Oud-Binnen_Maaiveld_Oud)
                *Binnen_Talud_Oud-Kruin_Breedte_Nieuw)
        /(Kruin_Hoogte_Oud+dH)
        """
        _mid_operand = base_data.polderside_slope * (
            base_data.crest_height - base_data.polderside_ground_level
        )
        _operand = base_data.crest_width + _mid_operand - scenario.crest_width
        _dividend = (
            base_data.crest_height - base_data.polderside_ground_level + scenario.d_h
        )
        return _operand / _dividend

    def _calculate_new_waterside_slope(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        """
        Kruin_Hoogte_Oud*Buiten_Talud_Oud
        /(Kruin_Hoogte_Oud+dH)
        """
        _operand = (
            base_data.crest_height - base_data.waterside_ground_level
        ) * base_data.waterside_slope
        _dividend = (
            base_data.crest_height - base_data.waterside_ground_level + scenario.d_h
        )
        return _operand / _dividend

    def _calculate_length_cofferdam(
        self,
        old_data: KoswatInputProfileProtocol,
        cofferdam_settings: KoswatCofferdamSettings,
        soil_polderside_berm_width: float,
        new_crest_height: float,
    ) -> float:
        """
        Identical to calculation of Stability wall
        """
        if soil_polderside_berm_width == 0:
            # Length of wall is not determined by piping.
            _length_piping = 0.0
        else:
            _length_piping = (
                (soil_polderside_berm_width / 6)
                + (new_crest_height - 0.5)
                - old_data.aquifer
            )
        _length_stability = (new_crest_height - 0.5) - (old_data.pleistocene - 1)
        return round(
            min(
                max(
                    _length_piping,
                    _length_stability,
                    cofferdam_settings.min_length_cofferdam,
                ),
                cofferdam_settings.max_length_cofferdam,
            ),
            1,
        )

    def _determine_construction_type(
        self,
        construction_length: float,
    ) -> ConstructionTypeEnum | None:
        if construction_length == 0:
            return None
        else:
            return ConstructionTypeEnum.KISTDAM

    def _calculate_new_input_profile(
        self,
        base_data: KoswatInputProfileBase,
        cofferdam_settings: KoswatCofferdamSettings,
        scenario: KoswatScenario,
    ) -> CofferDamInputProfile:
        _new_data = CofferDamInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.waterside_ground_level = base_data.waterside_ground_level
        _new_data.waterside_slope = self._calculate_new_waterside_slope(
            base_data, scenario
        )
        _new_data.waterside_berm_height = base_data.waterside_berm_height
        _new_data.waterside_berm_width = base_data.waterside_berm_width
        _new_data.crest_height = self._calculate_new_crest_height(base_data, scenario)
        _new_data.crest_width = scenario.crest_width
        _new_data.polderside_slope = self._calculate_new_polderside_slope(
            base_data, scenario
        )
        _new_data.polderside_berm_width = 0
        _new_data.polderside_berm_height = base_data.polderside_ground_level
        _new_data.polderside_ground_level = base_data.polderside_ground_level
        _soil_polderside_berm_width = self._calculate_soil_polderside_berm_width(
            base_data, _new_data, scenario
        )
        _new_data.ground_price_builtup = base_data.ground_price_builtup
        _new_data.ground_price_unbuilt = base_data.ground_price_unbuilt
        _new_data.factor_settlement = base_data.factor_settlement
        _new_data.pleistocene = base_data.pleistocene
        _new_data.aquifer = base_data.aquifer
        _new_data.construction_length = self._calculate_length_cofferdam(
            base_data,
            cofferdam_settings,
            _soil_polderside_berm_width,
            _new_data.crest_height,
        )
        _new_data.construction_type = self._determine_construction_type(
            _new_data.construction_length
        )
        _new_data.soil_surtax_factor = cofferdam_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = (
            cofferdam_settings.constructive_surtax_factor
        )
        _new_data.land_purchase_surtax_factor = None
        return _new_data

    def build(self) -> CofferDamInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data,
            self.reinforcement_settings.cofferdam_settings,
            self.scenario,
        )
