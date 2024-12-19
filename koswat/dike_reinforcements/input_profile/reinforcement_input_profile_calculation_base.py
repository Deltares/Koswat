from abc import ABC

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


class ReinforcementInputProfileCalculationBase(ABC):
    """
    Abstract class to provide common functions to child classes
    """

    def _get_reinforcement_profile(
        self,
        profile_type: type[KoswatInputProfileProtocol],
        base_data: KoswatInputProfileProtocol,
        scenario: KoswatScenario,
    ) -> KoswatInputProfileProtocol:
        """
        Create a new reinforced profile based on the base data and the scenario.
        This method contains the standard calculations for the profile.

        Args:
            profile_type (type[KoswatInputProfileProtocol]): The type of the profile to create.
            base_data (KoswatInputProfileProtocol): The base data to use for the calculations.
            scenario (KoswatScenario): The scenario to use for the calculations.

        Returns:
            KoswatInputProfileProtocol: The created reinforcement profile with standard properties populated.
        """
        _reinforced_profile = profile_type()

        _reinforced_profile.dike_section = base_data.dike_section

        _reinforced_profile.waterside_ground_level = base_data.waterside_ground_level
        _reinforced_profile.waterside_slope = self._calculate_new_waterside_slope(
            base_data, scenario
        )
        _reinforced_profile.waterside_berm_height = (
            self._calculate_new_waterside_berm_height(base_data, scenario)
        )
        _reinforced_profile.waterside_berm_width = base_data.waterside_berm_width

        _reinforced_profile.polderside_ground_level = base_data.polderside_ground_level

        _reinforced_profile.crest_width = scenario.crest_width
        _reinforced_profile.crest_height = self._calculate_new_crest_height(
            base_data, scenario
        )

        _reinforced_profile.ground_price_builtup = base_data.ground_price_builtup
        _reinforced_profile.ground_price_unbuilt = base_data.ground_price_unbuilt
        _reinforced_profile.factor_settlement = base_data.factor_settlement
        _reinforced_profile.pleistocene = base_data.pleistocene
        _reinforced_profile.aquifer = base_data.aquifer

        return _reinforced_profile

    @staticmethod
    def _calculate_new_waterside_slope(
        base_data: KoswatInputProfileProtocol, scenario: KoswatScenario
    ) -> float:
        return scenario.waterside_slope

    @staticmethod
    def _calculate_new_crest_height(
        base_data: KoswatInputProfileProtocol, scenario: KoswatScenario
    ) -> float:
        return base_data.crest_height + scenario.d_h

    @staticmethod
    def _calculate_new_waterside_berm_height(
        base_data: KoswatInputProfileProtocol, scenario: KoswatScenario
    ) -> float:
        if base_data.waterside_berm_height > base_data.waterside_ground_level:
            return base_data.waterside_berm_height + scenario.d_h
        return base_data.waterside_berm_height

    @staticmethod
    def _calculate_new_polderside_berm_height_piping(
        old_data: KoswatInputProfileProtocol,
        new_data: KoswatInputProfileProtocol,
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
