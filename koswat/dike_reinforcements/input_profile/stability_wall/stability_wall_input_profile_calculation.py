from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.configuration.settings.reinforcements.koswat_stability_wall_settings import (
    KoswatStabilityWallSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)


class StabilityWallInputProfileCalculation(
    ReinforcementInputProfileCalculationBase,
    ReinforcementInputProfileCalculationProtocol,
):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_length_stability_wall(
        self,
        old_data: KoswatInputProfileProtocol,
        stability_wall_settings: KoswatStabilityWallSettings,
        soil_polderside_berm_width: float,
        new_crest_height: float,
    ) -> float:
        """
        Identical to calculation of Cofferdam
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
                    stability_wall_settings.min_length_stability_wall,
                ),
                stability_wall_settings.max_length_stability_wall,
            ),
            1,
        )

    def _calculate_new_crest_height(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.crest_height + scenario.d_h

    def _calculate_new_polderside_slope(
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
            base_data.crest_height - base_data.polderside_ground_level
        ) * base_data.polderside_slope
        _second_part = scenario.d_h * scenario.waterside_slope
        _operand = (
            base_data.crest_width + _first_part - _second_part - scenario.crest_width
        )
        _dividend = (
            base_data.crest_height - base_data.polderside_ground_level + scenario.d_h
        )
        _right_side = _operand / _dividend
        return max(2, _right_side)

    def _determine_construction_type(
        self,
        overgang: float,
        construction_length: float,
    ) -> ConstructionTypeEnum | None:
        if construction_length == 0:
            return None
        elif construction_length <= overgang:
            return ConstructionTypeEnum.DAMWAND_VERANKERD
        else:
            return ConstructionTypeEnum.DIEPWAND

    def _calculate_new_input_profile(
        self,
        base_data: KoswatInputProfileProtocol,
        stability_wall_settings: KoswatStabilityWallSettings,
        scenario: KoswatScenario,
    ) -> StabilityWallInputProfile:
        _new_data = StabilityWallInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.waterside_ground_level = base_data.waterside_ground_level
        _new_data.waterside_slope = scenario.waterside_slope
        _new_data.waterside_berm_height = base_data.waterside_berm_height
        _new_data.waterside_berm_width = base_data.waterside_berm_width
        _new_data.crest_height = self._calculate_new_crest_height(base_data, scenario)
        _new_data.crest_width = scenario.crest_width
        _new_data.polderside_slope = self._calculate_new_polderside_slope(
            base_data, scenario
        )
        _new_data.polderside_berm_height = base_data.polderside_ground_level
        _new_data.polderside_berm_width = 0
        _new_data.polderside_ground_level = base_data.polderside_ground_level
        _new_data.ground_price_builtup = base_data.ground_price_builtup
        _new_data.ground_price_unbuilt = base_data.ground_price_unbuilt
        _new_data.factor_settlement = base_data.factor_settlement
        _new_data.pleistocene = base_data.pleistocene
        _new_data.aquifer = base_data.aquifer
        _soil_polderside_berm_width = self._calculate_soil_polderside_berm_width(
            base_data, _new_data, scenario
        )
        _new_data.construction_length = self._calculate_length_stability_wall(
            base_data,
            stability_wall_settings,
            _soil_polderside_berm_width,
            _new_data.crest_height,
        )
        _new_data.construction_type = self._determine_construction_type(
            stability_wall_settings.transition_sheetpile_diaphragm_wall,
            _new_data.construction_length,
        )
        _new_data.soil_surtax_factor = stability_wall_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = (
            stability_wall_settings.constructive_surtax_factor
        )
        _new_data.land_purchase_surtax_factor = (
            stability_wall_settings.land_purchase_surtax_factor
        )
        return _new_data

    def build(self) -> StabilityWallInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data,
            self.reinforcement_settings.stability_wall_settings,
            self.scenario,
        )
