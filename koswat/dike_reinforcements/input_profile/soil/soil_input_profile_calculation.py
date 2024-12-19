from dataclasses import asdict

from koswat.configuration.settings import KoswatScenario
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
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile import (
    SoilInputProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_factory import (
    BermCalculatorFactory,
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

    def build(self) -> SoilInputProfile:
        self.reinforced_data = SoilInputProfile()

        # Standard calculations
        self.populate_profile(self.base_profile.input_data, self.scenario)

        # Berm calculation
        _polderside_berm_calculator = BermCalculatorFactory(
            self.base_profile.input_data,
            self.reinforced_data,
            self.reinforcement_settings,
            self.scenario,
        ).get_berm_calculator(InputProfileEnum.SOIL)
        (
            self.reinforced_data.polderside_berm_width,
            self.reinforced_data.polderside_berm_height,
            self.reinforced_data.polderside_slope,
        ) = asdict(
            _polderside_berm_calculator.calculate(
                self.base_profile.input_data, self.reinforced_data
            )
        ).values()

        # Settings
        self.reinforced_data.soil_surtax_factor = (
            self.reinforcement_settings.soil_settings.soil_surtax_factor
        )
        self.reinforced_data.constructive_surtax_factor = None
        self.reinforced_data.land_purchase_surtax_factor = (
            self.reinforcement_settings.soil_settings.land_purchase_surtax_factor
        )

        return self.reinforced_data
