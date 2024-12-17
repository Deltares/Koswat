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
    base_data: KoswatInputProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario
    _dikebase_piping_old: float
    _dikebase_piping_new: float
    _dikebase_piping_new_vps: float
    _dikebase_height_new: float
    _dikebase_stability_new: float
    _berm_old_is_stability: bool
    _berm_factor_old: float
    _dike_height_new: float

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

    def _calculate_factors(self) -> None:
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
            self.base_data.crest_height - self.base_data.polderside_ground_level
        )
        self._dikebase_height_new = (
            self.scenario.d_h * self.base_data.waterside_slope
            + self.base_data.crest_width
            + self._dike_height_new * self.base_data.polderside_slope
        )
        self._dikebase_stability_new = _dikebase_stability_old + self.scenario.d_s

        self._dikebase_piping_new = self._dikebase_piping_old + self.scenario.d_p
        # Additionally calculate the dikebase piping for the VPS
        self._dikebase_piping_new_vps = max(
            self._dikebase_piping_old,
            max(self._dikebase_height_new, self._dikebase_stability_new)
            + self.reinforcement_settings.vps_settings.polderside_berm_width_vps,
        )

    def get_berm_calculator(
        self, profile_type: InputProfileEnum
    ) -> BermCalculatorProtocol:

        if profile_type == InputProfileEnum.COFFERDAM:
            return KeepBermCalculator(scenario=self.scenario)

        if profile_type == InputProfileEnum.STABILITY_WALL:
            return self.get_stability_wall_berm_calculator()

        if self._dikebase_piping_new > max(
            self._dikebase_height_new, self._dikebase_stability_new
        ):
            return PipingBermCalculator(
                scenario=self.scenario,
                reinforcement_settings=self.reinforcement_settings,
                dikebase_piping_old=self._dikebase_piping_old,
                dikebase_piping_new=self._dikebase_piping_new,
                dikebase_height_new=self._dikebase_height_new,
                dikebase_stability_new=self._dikebase_stability_new,
                dike_height_new=self._dike_height_new,
            )
        if self._dikebase_stability_new > self._dikebase_height_new:
            if self._berm_old_is_stability:
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
            return NoBermCalculator(
                scenario=self.scenario,
                reinforcement_settings=self.reinforcement_settings,
                dikebase_piping_old=self._dikebase_piping_old,
                dikebase_piping_new=self._dikebase_piping_new,
                dikebase_height_new=self._dikebase_height_new,
                dikebase_stability_new=self._dikebase_stability_new,
                dike_height_new=self._dike_height_new,
            )
        return DefaultBermCalculator()

    def get_stability_wall_berm_calculator(self) -> BermCalculatorProtocol:
        if (
            max(self._dikebase_height_new, self._dikebase_stability_new)
            > self._dikebase_piping_old
        ):
            return NoBermCalculator(
                scenario=self.scenario,
                reinforcement_settings=self.reinforcement_settings,
                dikebase_piping_old=self._dikebase_piping_old,
                dikebase_piping_new=self._dikebase_piping_new,
                dikebase_height_new=self._dikebase_height_new,
                dikebase_stability_new=self._dikebase_stability_new,
                dike_height_new=self._dike_height_new,
            )
        if (
            max(self._dikebase_height_new, self._dikebase_stability_new)
            < self._dikebase_piping_old
        ):
            return PipingBermCalculator(
                scenario=self.scenario,
                reinforcement_settings=self.reinforcement_settings,
                dikebase_piping_old=self._dikebase_piping_old,
                dikebase_piping_new=self._dikebase_piping_new,
                dikebase_height_new=self._dikebase_height_new,
                dikebase_stability_new=self._dikebase_stability_new,
                dike_height_new=self._dike_height_new,
            )
        if self._dikebase_stability_new > self._dikebase_height_new:
            if self._berm_old_is_stability:
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
            return NoBermCalculator(
                scenario=self.scenario,
                reinforcement_settings=self.reinforcement_settings,
                dikebase_piping_old=self._dikebase_piping_old,
                dikebase_piping_new=self._dikebase_piping_new,
                dikebase_height_new=self._dikebase_height_new,
                dikebase_stability_new=self._dikebase_stability_new,
                dike_height_new=self._dike_height_new,
            )
        return DefaultBermCalculator()
