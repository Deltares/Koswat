from abc import ABC

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class ReinforcementInputProfileCalculationBase(ABC):
    reinforced_data: KoswatInputProfileBase
    """
    Abstract class to provide common functions to child classes
    """

    def populate_profile(
        self, base_data: KoswatInputProfileProtocol, scenario: KoswatScenario
    ) -> None:
        self.reinforced_data.dike_section = base_data.dike_section

        self.reinforced_data.waterside_ground_level = base_data.waterside_ground_level
        self.reinforced_data.waterside_slope = self._calculate_new_waterside_slope(
            base_data, scenario
        )
        self.reinforced_data.waterside_berm_height = (
            self._calculate_new_waterside_berm_height(base_data, scenario)
        )
        self.reinforced_data.waterside_berm_width = base_data.waterside_berm_width

        self.reinforced_data.polderside_ground_level = base_data.polderside_ground_level

        self.reinforced_data.crest_width = scenario.crest_width
        self.reinforced_data.crest_height = self._calculate_new_crest_height(
            base_data, scenario
        )

        self.reinforced_data.ground_price_builtup = base_data.ground_price_builtup
        self.reinforced_data.ground_price_unbuilt = base_data.ground_price_unbuilt
        self.reinforced_data.factor_settlement = base_data.factor_settlement
        self.reinforced_data.pleistocene = base_data.pleistocene
        self.reinforced_data.aquifer = base_data.aquifer

    @staticmethod
    def _calculate_new_waterside_slope(
        base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return scenario.waterside_slope

    @staticmethod
    def _calculate_new_crest_height(
        base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.crest_height + scenario.d_h

    @staticmethod
    def _calculate_new_waterside_berm_height(
        base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        if base_data.waterside_berm_height > base_data.waterside_ground_level:
            return base_data.waterside_berm_height + scenario.d_h
        return base_data.waterside_berm_height

    @staticmethod
    def _calculate_new_polderside_berm_height_piping(
        old_data: KoswatInputProfileBase,
        new_data: KoswatInputProfileBase,
        soil_settings: KoswatSoilSettings,
        berm_extend_existing: bool,
    ) -> float:
        if berm_extend_existing:
            _old_berm_height = (
                old_data.polderside_berm_height - old_data.polderside_ground_level
            )
        else:
            _old_berm_height = 0.0

        _max = max(
            soil_settings.min_berm_height,
            _old_berm_height,
            new_data.polderside_berm_width * soil_settings.factor_increase_berm_height,
        )

        return (
            min(
                _max,
                soil_settings.max_berm_height_factor
                * (new_data.crest_height - new_data.polderside_ground_level),
            )
            + new_data.polderside_ground_level
        )
