from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.configuration.settings.reinforcements.koswat_vps_settings import (
    KoswatVPSSettings,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile_calculation import (
    SoilInputProfileCalculation,
)
from koswat.dike_reinforcements.input_profile.vertical_piping_solution.vps_input_profile import (
    VPSInputProfile,
)


class VPSInputProfileCalculation(
    SoilInputProfileCalculation,
    ReinforcementInputProfileCalculationProtocol,
):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def _calculate_new_input_profile(
        self,
        base_data: KoswatInputProfileBase,
        vps_settings: KoswatVPSSettings,
        scenario: KoswatScenario,
    ) -> KoswatInputProfileBase:
        _new_data = VPSInputProfile()
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
        _new_data.polderside_berm_width = vps_settings.polderside_berm_width_vps
        _new_data.polderside_berm_height = self._calculate_new_binnen_berm_hoogte(
            base_data, _new_data, scenario
        )
        _new_data.ground_price_builtup = base_data.ground_price_builtup
        _new_data.ground_price_unbuilt = base_data.ground_price_unbuilt
        _new_data.factor_settlement = base_data.factor_settlement
        _new_data.pleistocene = base_data.pleistocene
        _new_data.aquifer = base_data.aquifer
        _new_data.construction_type = ConstructionTypeEnum.VZG
        _new_data.soil_surtax_factor = vps_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = vps_settings.constructive_surtax_factor
        _new_data.land_purchase_surtax_factor = vps_settings.land_purchase_surtax_factor
        return _new_data

    def build(self) -> VPSInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data,
            self.reinforcement_settings.vps_settings,
            self.scenario,
        )
