from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)


class PipingWallInputProfileCalculation(
    ReinforcementInputProfileCalculationBase,
    ReinforcementInputProfileCalculationProtocol,
):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_length_piping_wall(
        self,
        old_data: KoswatInputProfileBase,
        piping_wall_settings: KoswatPipingWallSettings,
        soil_binnen_berm_breedte: float,
    ) -> float:
        if soil_binnen_berm_breedte == 0:
            # No wall is needed.
            return 0
        _length_piping = (
            (soil_binnen_berm_breedte / 6)
            + (old_data.binnen_maaiveld - old_data.aquifer)
            + 1
        )
        return round(
            min(
                max(
                    _length_piping,
                    piping_wall_settings.min_length_piping_wall,
                ),
                piping_wall_settings.max_length_piping_wall,
            ),
            1,
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
            Binnen_Talud_Oud,
            (
                dS
                -dH*Buiten_Talud_Nieuw
                -(Kruin_Breedte_Nieuw-Kruin_Breedte_Oud)
                +(Kruin_Hoogte_Oud-Binnen_Maaiveld_Oud)*Binnen_Talud_Oud)
                /(Kruin_Hoogte_Oud-Binnen_Maaiveld_Oud+dH))
        """
        _first_part = scenario.d_h * scenario.polderside_slope
        _second_part = scenario.crest_width - base_data.kruin_breedte
        _third_parth = (
            base_data.kruin_hoogte - base_data.binnen_maaiveld
        ) * base_data.binnen_talud
        _dividend = base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h
        _right_side = (
            scenario.d_s - _first_part - _second_part + _third_parth
        ) / _dividend
        return max(base_data.binnen_talud, _right_side)

    def _determine_construction_type(
        self, overgang: float, construction_length: float
    ) -> ConstructionTypeEnum | None:
        if construction_length == 0:
            return None
        elif construction_length <= overgang:
            return ConstructionTypeEnum.CB_DAMWAND
        else:
            return ConstructionTypeEnum.DAMWAND_ONVERANKERD

    def _calculate_new_input_profile(
        self,
        base_data: KoswatInputProfileBase,
        piping_wall_settings: KoswatPipingWallSettings,
        scenario: KoswatScenario,
    ) -> PipingWallInputProfile:
        _new_data = PipingWallInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.buiten_talud = scenario.polderside_slope
        _new_data.buiten_berm_hoogte = base_data.buiten_berm_hoogte
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte
        _new_data.kruin_hoogte = self._calculate_new_kruin_hoogte(base_data, scenario)
        _new_data.kruin_breedte = scenario.crest_width
        _new_data.binnen_talud = self._calculate_new_binnen_talud(base_data, scenario)
        _new_data.binnen_berm_hoogte = base_data.binnen_maaiveld
        _new_data.binnen_berm_breedte = 0
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        _soil_binnen_berm_breedte = self._calculate_soil_binnen_berm_breedte(
            base_data, _new_data, scenario
        )
        _new_data.grondprijs_bebouwd = base_data.grondprijs_bebouwd
        _new_data.grondprijs_onbebouwd = base_data.grondprijs_onbebouwd
        _new_data.factor_zetting = base_data.factor_zetting
        _new_data.pleistoceen = base_data.pleistoceen
        _new_data.aquifer = base_data.aquifer
        _new_data.construction_length = self._calculate_length_piping_wall(
            base_data, piping_wall_settings, _soil_binnen_berm_breedte
        )
        _new_data.construction_type = self._determine_construction_type(
            piping_wall_settings.transition_cbwall_sheetpile,
            _new_data.construction_length,
        )
        _new_data.soil_surtax_factor = piping_wall_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = (
            piping_wall_settings.constructive_surtax_factor
        )
        _new_data.land_purchase_surtax_factor = (
            piping_wall_settings.land_purchase_surtax_factor
        )
        return _new_data

    def build(self) -> PipingWallInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data,
            self.reinforcement_settings.piping_wall_settings,
            self.scenario,
        )
