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
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_factory import (
    BermCalculatorFactory,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.no_berm_calculator import (
    NoBermCalculator,
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

    @staticmethod
    def _calculate_length_stability_wall(
        old_data: KoswatInputProfileProtocol,
        stability_wall_settings: KoswatStabilityWallSettings,
        seepage_length: float,
        stab_wall: bool,
        new_crest_height: float,
    ) -> float:
        if stab_wall:
            _length_stability = (new_crest_height - 0.5) - (old_data.pleistocene - 1)
            if seepage_length == 0:
                # Length of wall is not determined by piping.
                _length_piping = 0.0
            else:
                _length_piping = (
                    (seepage_length / 6) + (new_crest_height - 0.5) - old_data.aquifer
                )
        else:
            _length_stability = 0
            if seepage_length == 0:
                # Length of wall is not determined by piping.
                _length_piping = 0.0
            else:
                # Length of wall zoals bij kwelscherm
                _length_piping = (
                    (seepage_length / 6)
                    + (old_data.polderside_ground_level - old_data.aquifer)
                    + 1  # 1 m in bestaande dijklichaam
                )

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

    @staticmethod
    def _determine_construction_type(
        transition: float,
        construction_length: float,
    ) -> ConstructionTypeEnum | None:
        if construction_length == 0:
            return None
        if construction_length <= transition:
            return ConstructionTypeEnum.DAMWAND_VERANKERD
        return ConstructionTypeEnum.DIEPWAND

    def build(self) -> StabilityWallInputProfile:
        self.reinforced_data = StabilityWallInputProfile()

        # Standard calculations
        self.populate_profile(self.base_profile.input_data, self.scenario)

        # Berm calculation
        _polderside_berm_calculator = BermCalculatorFactory(
            self.base_profile.input_data, self.reinforcement_settings, self.scenario
        ).get_berm_calculator(InputProfileEnum.STABILITY_WALL)
        (
            self.reinforced_data.polderside_berm_width,
            self.reinforced_data.polderside_berm_height,
            self.reinforced_data.polderside_slope,
        ) = _polderside_berm_calculator.calculate(
            self.base_profile.input_data, self.reinforced_data
        )

        # Construction calculations
        _dikebase_piping_realized = (
            self.scenario.d_h * self.reinforced_data.waterside_slope
            + self.reinforced_data.crest_width
            + _polderside_berm_calculator.dike_height_new
            * self.reinforced_data.polderside_slope
            + self.reinforced_data.polderside_berm_width
        )
        _seepage_length = max(
            _polderside_berm_calculator.dikebase_piping_new - _dikebase_piping_realized,
            0,
        )
        _stab_wall = isinstance(_polderside_berm_calculator, NoBermCalculator)
        self.reinforced_data.construction_length = (
            self._calculate_length_stability_wall(
                self.base_profile.input_data,
                self.reinforcement_settings.stability_wall_settings,
                _seepage_length,
                _stab_wall,
                self.reinforced_data.crest_height,
            )
        )
        self.reinforced_data.construction_type = self._determine_construction_type(
            self.reinforcement_settings.stability_wall_settings.transition_sheetpile_diaphragm_wall,
            self.reinforced_data.construction_length,
        )

        # Settings
        self.reinforced_data.soil_surtax_factor = (
            self.reinforcement_settings.stability_wall_settings.soil_surtax_factor
        )
        self.reinforced_data.constructive_surtax_factor = (
            self.reinforcement_settings.stability_wall_settings.constructive_surtax_factor
        )
        self.reinforced_data.land_purchase_surtax_factor = (
            self.reinforcement_settings.stability_wall_settings.land_purchase_surtax_factor
        )

        return self.reinforced_data
