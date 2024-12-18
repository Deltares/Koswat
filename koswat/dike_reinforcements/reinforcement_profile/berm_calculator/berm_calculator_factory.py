from collections import defaultdict

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator import (
    BermCalculatorProtocol,
    DefaultBermCalculator,
    KeepBermCalculator,
    NoBermCalculator,
    PipingBermCalculator,
    StabilityBermCalculator,
)


class BermCalculatorFactory:
    """
    Factory to create the correct berm calculator based on the base profile,
    reinforcement settings, scenario and profile type.
    """

    base_data: KoswatInputProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario
    _dikebase_piping_old: float
    _dikebase_piping_new_dict: dict[InputProfileEnum, float] = defaultdict(float)
    _dikebase_height_new: float
    _dikebase_stability_new: float
    _berm_old_is_stability: bool
    _berm_factor_old: float
    _dike_height_new: float
    _reinforcement_type: InputProfileEnum

    def __init__(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforcement_settings: KoswatReinforcementSettings,
        scenario: KoswatScenario,
    ) -> None:
        self.base_data = base_data
        self.reinforcement_settings = reinforcement_settings
        self.scenario = scenario

        self._calculate_factors()

    @property
    def _dikebase_piping_new(self):
        if self._reinforcement_type in self._dikebase_piping_new_dict.keys():
            return self._dikebase_piping_new_dict[self._reinforcement_type]
        return self._dikebase_piping_new_dict[InputProfileEnum.NONE]

    def _calculate_new_crest_height(self) -> float:
        return self.base_data.crest_height + self.scenario.d_h

    def _calculate_factors(self):
        _dike_height_old = (
            self.base_data.crest_height - self.base_data.polderside_ground_level
        )
        _berm_height_old = (
            self.base_data.polderside_berm_height
            - self.base_data.polderside_ground_level
        )
        self._berm_factor_old = _berm_height_old / _dike_height_old
        self._berm_old_is_stability = (
            self._berm_factor_old
            > self.reinforcement_settings.soil_settings.max_berm_height_factor
        )

        _dikebase_stability_old = (
            self.base_data.crest_width
            + _dike_height_old * self.base_data.polderside_slope
            + self._berm_old_is_stability * self.base_data.polderside_berm_width
        )
        self._dikebase_piping_old = (
            self.base_data.crest_width
            + _dike_height_old * self.base_data.polderside_slope
            + self.base_data.polderside_berm_width
        )

        self._dike_height_new = (
            self._calculate_new_crest_height() - self.base_data.polderside_ground_level
        )
        self._dikebase_height_new = (
            self.scenario.d_h * self.base_data.waterside_slope
            + self.base_data.crest_width
            + self._dike_height_new * self.base_data.polderside_slope
        )
        self._dikebase_stability_new = _dikebase_stability_old + self.scenario.d_s

        self._dikebase_piping_new_dict[InputProfileEnum.NONE] = (
            self._dikebase_piping_old + self.scenario.d_p
        )
        self._dikebase_piping_new_dict[InputProfileEnum.PIPING_WALL] = max(
            self._dikebase_piping_old,
            self._dikebase_height_new,
            self._dikebase_stability_new,
        )
        self._dikebase_piping_new_dict[InputProfileEnum.VPS] = max(
            self._dikebase_piping_old,
            max(self._dikebase_height_new, self._dikebase_stability_new)
            + self.reinforcement_settings.vps_settings.polderside_berm_width_vps,
        )

    def get_berm_calculator(
        self, profile_type: InputProfileEnum
    ) -> BermCalculatorProtocol:
        """
        Get the correct berm calculator based on the profile type.

        Args:
            profile_type (InputProfileEnum): The type of profile.

        Returns:
            BermCalculatorProtocol: The correct berm calculator.
        """

        self._reinforcement_type = profile_type

        if profile_type == InputProfileEnum.COFFERDAM:
            return self._get_keep_berm_calculator()

        if profile_type == InputProfileEnum.STABILITY_WALL:
            return self._get_stability_wall_berm_calculator()

        if self._dikebase_piping_new > max(
            self._dikebase_height_new, self._dikebase_stability_new
        ):
            return self._get_piping_berm_calculator()

        if self._dikebase_stability_new > self._dikebase_height_new:
            if self._berm_old_is_stability:
                return self._get_stability_berm_calculator()
            return self._get_no_berm_calculator()

        return self._get_default_berm_calculator()

    def _get_stability_wall_berm_calculator(self) -> BermCalculatorProtocol:
        # The stability wall has different logic for the berm calculation
        if (
            max(self._dikebase_height_new, self._dikebase_stability_new)
            > self._dikebase_piping_old
        ):
            return self._get_no_berm_calculator()
        if (
            max(self._dikebase_height_new, self._dikebase_stability_new)
            < self._dikebase_piping_old
        ):
            return self._get_piping_berm_calculator()
        if self._dikebase_stability_new > self._dikebase_height_new:
            if self._berm_old_is_stability:
                return self._get_stability_berm_calculator()
            return self._get_no_berm_calculator()
        return self._get_default_berm_calculator()

    def _get_keep_berm_calculator(self) -> BermCalculatorProtocol:
        return KeepBermCalculator(
            scenario=self.scenario,
            dikebase_piping_old=self._dikebase_piping_old,
            dikebase_piping_new=self._dikebase_piping_new,
            dike_height_new=self._dike_height_new,
        )

    def _get_piping_berm_calculator(self) -> BermCalculatorProtocol:
        return PipingBermCalculator(
            scenario=self.scenario,
            reinforcement_settings=self.reinforcement_settings,
            dikebase_piping_old=self._dikebase_piping_old,
            dikebase_piping_new=self._dikebase_piping_new,
            dikebase_height_new=self._dikebase_height_new,
            dikebase_stability_new=self._dikebase_stability_new,
            dike_height_new=self._dike_height_new,
        )

    def _get_stability_berm_calculator(self) -> BermCalculatorProtocol:
        return StabilityBermCalculator(
            scenario=self.scenario,
            reinforcement_settings=self.reinforcement_settings,
            dikebase_piping_old=self._dikebase_piping_old,
            dikebase_piping_new=self._dikebase_piping_new,
            dikebase_height_new=self._dikebase_height_new,
            dikebase_stability_new=self._dikebase_stability_new,
            dike_height_new=self._dike_height_new,
            berm_factor_old=self._berm_factor_old,
        )

    def _get_no_berm_calculator(self) -> BermCalculatorProtocol:
        return NoBermCalculator(
            scenario=self.scenario,
            reinforcement_settings=self.reinforcement_settings,
            dikebase_piping_old=self._dikebase_piping_old,
            dikebase_piping_new=self._dikebase_piping_new,
            dikebase_height_new=self._dikebase_height_new,
            dikebase_stability_new=self._dikebase_stability_new,
            dike_height_new=self._dike_height_new,
            reinforcement_type=self._reinforcement_type,
        )

    def _get_default_berm_calculator(self) -> BermCalculatorProtocol:
        return DefaultBermCalculator(
            dikebase_piping_old=self._dikebase_piping_old,
            dikebase_piping_new=self._dikebase_piping_new,
            dike_height_new=self._dike_height_new,
        )
