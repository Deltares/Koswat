from koswat.configuration.settings import KoswatScenario
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.input_profile import (
    PipingWallInputProfileCalculation,
    SoilInputProfileCalculation,
    StabilityWallInputProfileCalculation,
    VPSInputProfileCalculation,
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
from koswat.dike_reinforcements.reinforcement_layers.standard_reinforcement_layers_wrapper_builder import (
    StandardReinforcementLayersWrapperBuilder,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_builder_base import (
    ReinforcementProfileBuilderBase,
)
from koswat.dike_reinforcements.reinforcement_profile.standard import (
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.vps_reinforcement_profile import (
    VPSReinforcementProfile,
)


class StandardReinforcementProfileBuilder(ReinforcementProfileBuilderBase):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: type[StandardReinforcementProfile]

    @staticmethod
    def get_input_profile_calculator(
        reinforcement_type: type[StandardReinforcementProfile],
    ) -> ReinforcementInputProfileCalculationProtocol:
        """
        Get the input profile calculator for the given reinforcement type.

        Args:
            reinforcement_type (type[StandardReinforcementProfile]): The reinforcement type.

        Raises:
            NotImplementedError: The given reinforcement type is not supported.

        Returns:
            ReinforcementInputProfileCalculationProtocol: The input profile calculator.
        """
        if issubclass(reinforcement_type, SoilReinforcementProfile):
            return SoilInputProfileCalculation()
        if issubclass(reinforcement_type, VPSReinforcementProfile):
            return VPSInputProfileCalculation()
        if issubclass(reinforcement_type, PipingWallReinforcementProfile):
            return PipingWallInputProfileCalculation()
        if issubclass(reinforcement_type, StabilityWallReinforcementProfile):
            return StabilityWallInputProfileCalculation()
        raise NotImplementedError(f"Type {reinforcement_type} not supported.")

    def _get_reinforcement_layers_wrapper(
        self, profile_points: CharacteristicPoints
    ) -> ReinforcementLayersWrapper:
        _unchanged_outside_slope = (
            self.scenario.waterside_slope == self.base_profile.input_data.buiten_talud
        )
        _layers_builder = (
            StandardReinforcementLayersWrapperBuilder()
            if _unchanged_outside_slope
            else OutsideSlopeReinforcementLayersWrapperBuilder()
        )
        _layers_builder.layers_data = self.base_profile.layers_wrapper.as_data_dict()
        _layers_builder.profile_points = profile_points.points
        return _layers_builder.build()

    def _get_characteristic_points(
        self,
        input_profile: ReinforcementInputProfileProtocol,
    ) -> CharacteristicPoints:
        _char_points_builder = CharacteristicPointsBuilder()
        _char_points_builder.input_profile = input_profile
        _char_points_builder.p4_x_coordinate = (
            self.scenario.d_h * self.scenario.waterside_slope
        )
        return _char_points_builder.build()
