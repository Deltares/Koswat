from typing import Type

from koswat.calculations.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.calculations.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_reinforcement_profile_calculation import (
    PipingWallReinforcementProfileCalculation,
)
from koswat.calculations.standard_reinforcement.soil.soil_reinforcement_profile_calculation import (
    SoilReinforcementProfileCalculation,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_reinforcement_profile_calculation import (
    StabilityWallReinforcementProfileCalculation,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfile,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.koswat_scenario import KoswatScenario


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
        elif issubclass(reinforcement_type, ReinforcementProfileProtocol):
            return SoilReinforcementProfileCalculation
        elif issubclass(reinforcement_type, StabilityWallReinforcementProfile):
            return StabilityWallReinforcementProfileCalculation
        else:
            raise NotImplementedError(f"Type {reinforcement_type} not supported.")

    def _get_reinforcment_profile_input(self) -> ReinforcementInputProfileProtocol:
        _calculator = self.get_standard_reinforcement_calculator(
            self.reinforcement_profile_type
        )()
        _calculator.base_profile = self.base_profile
        _calculator.scenario = self.scenario
        return _calculator.build()

    def build(self) -> StandardReinforcementProfile:
        _input_profile = self._get_reinforcment_profile_input()
        # _data_layers = self.base_profile.layers_wrapper.as_data_dict()
        # _builder_dict = dict(
        #     input_profile_data=_new_data.__dict__,
        #     layers_data=_data_layers,
        #     p4_x_coordinate=self.scenario.d_h * self.scenario.buiten_talud,
        #     profile_type=PipingWallReinforcementProfile,
        # )
        # return KoswatProfileBuilder.with_data(_builder_dict).build()

        return super().build()
