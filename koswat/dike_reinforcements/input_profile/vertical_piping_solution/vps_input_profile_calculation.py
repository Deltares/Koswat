from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.vertical_piping_solution.vps_input_profile import (
    VPSInputProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_factory import (
    BermCalculatorFactory,
)


class VPSInputProfileCalculation(
    ReinforcementInputProfileCalculationBase,
    ReinforcementInputProfileCalculationProtocol,
):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def build(self) -> VPSInputProfile:
        self.reinforced_data = VPSInputProfile()

        # Standard calculations
        self.populate_profile(self.base_profile.input_data, self.scenario)

        # Berm calculations
        _polderside_berm_calculator = BermCalculatorFactory(
            self.base_profile.input_data, self.reinforcement_settings, self.scenario
        ).get_berm_calculator(InputProfileEnum.VPS)
        (
            self.reinforced_data.polderside_berm_width,
            self.reinforced_data.polderside_berm_height,
            self.reinforced_data.polderside_slope,
        ) = _polderside_berm_calculator.calculate(
            self.base_profile.input_data, self.reinforced_data
        )

        # Construction calculations
        self.reinforced_data.construction_type = ConstructionTypeEnum.VZG

        # Settings
        self.reinforced_data.soil_surtax_factor = (
            self.reinforcement_settings.vps_settings.soil_surtax_factor
        )
        self.reinforced_data.constructive_surtax_factor = (
            self.reinforcement_settings.vps_settings.constructive_surtax_factor
        )
        self.reinforced_data.land_purchase_surtax_factor = (
            self.reinforcement_settings.vps_settings.land_purchase_surtax_factor
        )

        return self.reinforced_data
