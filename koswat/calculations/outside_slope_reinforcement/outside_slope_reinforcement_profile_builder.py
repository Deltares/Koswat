from typing import Type

from koswat.calculations.outside_slope_reinforcement.cofferdam import (
    CofferdamReinforcementProfile,
    CofferdamReinforcementProfileCalculation,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_layers_wrapper_builder import (
    OutsideSlopeReinforcementLayersWrapperBuilder,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)
from koswat.calculations.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.calculations.reinforcement_layers_wrapper import ReinforcementLayersWrapper
from koswat.calculations.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.koswat_scenario import KoswatScenario


class OutsideSlopeReinforcementProfileBuilder(ReinforcementProfileBuilderProtocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: Type[OutsideSlopeReinforcementProfile]

    @staticmethod
    def get_standard_reinforcement_calculator(
        reinforcement_type: Type[OutsideSlopeReinforcementProfile],
    ):
        if issubclass(reinforcement_type, CofferdamReinforcementProfile):
            return CofferdamReinforcementProfileCalculation
        else:
            raise NotImplementedError(f"Type {reinforcement_type} not supported.")

    def _get_reinforcement_profile_input(
        self,
    ) -> ReinforcementInputProfileCalculationProtocol:
        _calculator = self.get_standard_reinforcement_calculator(
            self.reinforcement_profile_type
        )()
        _calculator.base_profile = self.base_profile
        _calculator.scenario = self.scenario
        return _calculator.build()

    def _get_reinforcement_layers_wrapper(
        self, profile_points: CharacteristicPoints
    ) -> ReinforcementLayersWrapper:
        _layers_builder = OutsideSlopeReinforcementLayersWrapperBuilder()
        _layers_builder.layers_data = self.base_profile.layers_wrapper.as_data_dict()
        _layers_builder.profile_points = profile_points.points
        return _layers_builder.build()

    def _get_characteristic_points(
        self, input_profile: ReinforcementInputProfileProtocol
    ) -> CharacteristicPoints:
        _char_points_builder = CharacteristicPointsBuilder()
        _char_points_builder.input_profile = input_profile
        _char_points_builder.p4_x_coordinate = 0
        return _char_points_builder.build()

    def build(self) -> OutsideSlopeReinforcementProfile:
        _profile = self.reinforcement_profile_type()
        _profile.input_data = self._get_reinforcement_profile_input()
        _profile.characteristic_points = self._get_characteristic_points(
            _profile.input_data
        )
        _profile.layers_wrapper = self._get_reinforcement_layers_wrapper(
            _profile.characteristic_points
        )
        return _profile
