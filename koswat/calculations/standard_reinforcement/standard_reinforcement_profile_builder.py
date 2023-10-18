from __future__ import annotations

import logging
import math
from typing import Type

from koswat.calculations.protocols import (
    ReinforcementInputProfileProtocol,
    ReinforcementProfileBuilderProtocol,
)
from koswat.calculations.reinforcement_layers_wrapper import ReinforcementLayersWrapper
from koswat.calculations.standard_reinforcement import (
    PipingWallReinforcementProfile,
    PipingWallReinforcementProfileCalculation,
    SoilReinforcementProfile,
    SoilReinforcementProfileCalculation,
    StabilityWallReinforcementProfile,
    StabilityWallReinforcementProfileCalculation,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_layers_wrapper_builder import (
    StandardReinforcementLayersWrapperBuilder,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class StandardReinforcementProfileBuilder(ReinforcementProfileBuilderProtocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: Type[StandardReinforcementProfile]

    @staticmethod
    def get_standard_reinforcement_calculator(
        reinforcement_type: Type[StandardReinforcementProfile],
    ):
        if issubclass(reinforcement_type, PipingWallReinforcementProfile):
            return PipingWallReinforcementProfileCalculation
        elif issubclass(reinforcement_type, SoilReinforcementProfile):
            return SoilReinforcementProfileCalculation
        elif issubclass(reinforcement_type, StabilityWallReinforcementProfile):
            return StabilityWallReinforcementProfileCalculation
        else:
            raise NotImplementedError(f"Type {reinforcement_type} not supported.")

    def _get_corrected_koswat_scenario(self) -> KoswatScenario:
        """
        Get a koswat scenario (`KoswatScenario`) whose values are not `math.nan`.
        In practice this means that when a `KoswatScenario` value has not been set
        the corresponding one from `KoswatProfileBase` will be used instead.

        Returns:
            KoswatScenario: Valid scenario to be used in reinforcements.
        """
        _new_koswat_scenario = KoswatScenario(**self.scenario.__dict__)
        if math.isnan(_new_koswat_scenario.kruin_breedte):
            _new_koswat_scenario.kruin_breedte = (
                self.base_profile.input_data.kruin_breedte
            )
        if math.isnan(_new_koswat_scenario.buiten_talud):
            _new_koswat_scenario.buiten_talud = (
                self.base_profile.input_data.buiten_talud
            )

        return _new_koswat_scenario

    def _get_reinforcement_profile_input(
        self, koswat_scenario: KoswatScenario
    ) -> ReinforcementInputProfileProtocol:
        _calculator = self.get_standard_reinforcement_calculator(
            self.reinforcement_profile_type
        )()
        _calculator.base_profile = self.base_profile
        _calculator.scenario = koswat_scenario
        return _calculator.build()

    def _get_characteristic_points(
        self,
        input_profile: ReinforcementInputProfileProtocol,
        koswat_scenario: KoswatScenario,
    ) -> CharacteristicPoints:
        _char_points_builder = CharacteristicPointsBuilder()
        _char_points_builder.input_profile = input_profile
        _char_points_builder.p4_x_coordinate = (
            koswat_scenario.d_h * koswat_scenario.buiten_talud
        )
        return _char_points_builder.build()

    def _get_reinforcement_layers_wrapper(
        self, profile_points: CharacteristicPoints
    ) -> ReinforcementLayersWrapper:
        _layers_builder = StandardReinforcementLayersWrapperBuilder()
        _layers_builder.layers_data = self.base_profile.layers_wrapper.as_data_dict()
        _layers_builder.profile_points = profile_points.points
        return _layers_builder.build()

    def build(self) -> StandardReinforcementProfile:
        _corrected_scenario = self._get_corrected_koswat_scenario()
        _profile = self.reinforcement_profile_type()
        logging.info("Building reinforcement {}".format(_profile))

        _profile.old_profile = self.base_profile
        _profile.input_data = self._get_reinforcement_profile_input(_corrected_scenario)
        _profile.characteristic_points = self._get_characteristic_points(
            _profile.input_data, _corrected_scenario
        )
        _profile.layers_wrapper = self._get_reinforcement_layers_wrapper(
            _profile.characteristic_points
        )
        logging.info("Generated reinforcement {}".format(_profile))

        return _profile
