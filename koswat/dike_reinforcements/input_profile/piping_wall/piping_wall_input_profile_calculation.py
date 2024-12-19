from dataclasses import asdict

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_factory import (
    BermCalculatorFactory,
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

    @staticmethod
    def _calculate_length_piping_wall(
        old_data: KoswatInputProfileProtocol,
        piping_wall_settings: KoswatPipingWallSettings,
        seepage_length: float,
    ) -> float:
        if seepage_length == 0.0:
            # No wall is needed.
            return 0.0
        _length_piping = (
            (seepage_length / 6.0)
            + (old_data.polderside_ground_level - old_data.aquifer)
            + 1.0
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

    @staticmethod
    def _determine_construction_type(
        transition: float, construction_length: float
    ) -> ConstructionTypeEnum | None:
        if construction_length == 0:
            return None
        if construction_length <= transition:
            return ConstructionTypeEnum.CB_DAMWAND
        return ConstructionTypeEnum.DAMWAND_ONVERANKERD

    def build(self) -> PipingWallInputProfile:
        self.reinforced_data = self._get_reinforcement_profile(
            PipingWallInputProfile, self.base_profile.input_data, self.scenario
        )
        assert isinstance(self.reinforced_data, PipingWallInputProfile)

        # Berm calculation
        _polderside_berm_calculator = BermCalculatorFactory(
            self.base_profile.input_data,
            self.reinforced_data,
            self.reinforcement_settings,
            self.scenario,
        ).get_berm_calculator(InputProfileEnum.PIPING_WALL)
        (
            self.reinforced_data.polderside_berm_width,
            self.reinforced_data.polderside_berm_height,
            self.reinforced_data.polderside_slope,
        ) = asdict(
            _polderside_berm_calculator.calculate(
                self.base_profile.input_data, self.reinforced_data
            )
        ).values()

        # Construction calculations
        _dikebase_piping_needed = (
            _polderside_berm_calculator.dikebase_piping_old + self.scenario.d_p
        )
        _seepage_length = max(
            _dikebase_piping_needed - _polderside_berm_calculator.dikebase_piping_new, 0
        )
        self.reinforced_data.construction_length = self._calculate_length_piping_wall(
            self.base_profile.input_data,
            self.reinforcement_settings.piping_wall_settings,
            _seepage_length,
        )
        self.reinforced_data.construction_type = self._determine_construction_type(
            self.reinforcement_settings.piping_wall_settings.transition_cbwall_sheetpile,
            self.reinforced_data.construction_length,
        )

        # Settings
        self.reinforced_data.soil_surtax_factor = (
            self.reinforcement_settings.piping_wall_settings.soil_surtax_factor
        )
        self.reinforced_data.constructive_surtax_factor = (
            self.reinforcement_settings.piping_wall_settings.constructive_surtax_factor
        )
        self.reinforced_data.land_purchase_surtax_factor = (
            self.reinforcement_settings.piping_wall_settings.land_purchase_surtax_factor
        )

        return self.reinforced_data
