from koswat.dike_reinforcements.reinforcement_layers.outside_slope_reinforcement_layers_wrapper_builder import (
    OutsideSlopeReinforcementLayersWrapperBuilder,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class OutsideSlopeReinforcementProfileBuilder(ReinforcementProfileBuilderProtocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario

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

    def build(self) -> ReinforcementProfile:
        _profile = ReinforcementProfile()
        _profile.old_profile = self.base_profile
        _profile.input_data = self._get_reinforcement_profile_input()
        _profile.characteristic_points = self._get_characteristic_points(
            _profile.input_data
        )
        _profile.layers_wrapper = self._get_reinforcement_layers_wrapper(
            _profile.characteristic_points
        )
        return _profile
