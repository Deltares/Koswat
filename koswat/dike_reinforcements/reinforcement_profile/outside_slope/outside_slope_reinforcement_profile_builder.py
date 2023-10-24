from koswat.configuration.settings import KoswatScenario
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile_calculation import (
    CofferdamInputProfileCalculation,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_layers.outside_slope_reinforcement_layers_wrapper_builder import (
    OutsideSlopeReinforcementLayersWrapperBuilder,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_builder_base import (
    ReinforcementProfileBuilderBase,
)


class OutsideSlopeReinforcementProfileBuilder(ReinforcementProfileBuilderBase):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: type[OutsideSlopeReinforcementProfile]

    @staticmethod
    def get_input_profile_calculator(
        reinforcement_type: type[OutsideSlopeReinforcementProfile],
    ) -> ReinforcementInputProfileCalculationProtocol:
        if issubclass(reinforcement_type, CofferdamReinforcementProfile):
            return CofferdamInputProfileCalculation()
        raise NotImplementedError(f"Type {reinforcement_type} not supported.")

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
