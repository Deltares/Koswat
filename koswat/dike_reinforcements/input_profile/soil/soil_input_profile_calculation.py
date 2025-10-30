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
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculated_factors import (
    BermCalculatedFactors,
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
        _reinforced_data = self._get_reinforcement_profile(
            SoilInputProfile, self.base_profile.input_data, self.scenario
        )
        assert isinstance(_reinforced_data, SoilInputProfile)
        
        _reinforced_data.active = self.reinforcement_settings.soil_settings.active

        # Berm calculation
        _calculated_factors = BermCalculatedFactors.from_calculation_input(
            self.base_profile.input_data,
            _reinforced_data,
            self.reinforcement_settings,
            self.scenario,
        )
        _polderside_berm_calculator = BermCalculatorFactory.get_berm_calculator(
            InputProfileEnum.SOIL, _calculated_factors
        )
        (
            _reinforced_data.polderside_berm_width,
            _reinforced_data.polderside_berm_height,
            _reinforced_data.polderside_slope,
        ) = asdict(
            _polderside_berm_calculator.calculate(
                self.base_profile.input_data, _reinforced_data
            )
        ).values()

        # Settings
        _reinforced_data.soil_surtax_factor = (
            self.reinforcement_settings.soil_settings.soil_surtax_factor
        )
        _reinforced_data.constructive_surtax_factor = None
        _reinforced_data.land_purchase_surtax_factor = (
            self.reinforcement_settings.soil_settings.land_purchase_surtax_factor
        )

        return _reinforced_data
