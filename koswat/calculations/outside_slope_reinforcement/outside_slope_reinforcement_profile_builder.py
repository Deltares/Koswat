from typing import Type

from koswat.calculations.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile_calculation import (
    CofferdamReinforcementProfileCalculation,
)
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfile,
)
from koswat.calculations.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
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

    def _get_reinforcement_layers_wrapper(self):
        pass

    def build(self) -> OutsideSlopeReinforcementProfile:
        _input_profile = self._get_reinforcement_profile_input()
        # _data_layers = self.base_profile.layers_wrapper.as_data_dict()
        # _builder_dict = dict(
        #     input_profile_data=_new_data.__dict__,
        #     layers_data=_data_layers,
        #     p4_x_coordinate=0,
        #     profile_type=CofferdamReinforcementProfile,
        # )
        # return KoswatProfileBuilder.with_data(_builder_dict).build()

        return super().build()
