from koswat.calculations.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario


class PipingWallReinforcementProfileCalculation(
    ReinforcementProfileCalculationProtocol
):
    base_profile: KoswatProfileProtocol
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_new_input_profile(self):
        pass

    def build(self) -> PipingWallReinforcementProfile:
        _new_data = self._calculate_new_input_profile(
            self.base_profile.input_data, self.scenario
        )
        _data_layers = self.base_profile.layers.as_data_dict()
        _builder_dict = dict(
            input_profile_data=_new_data.__dict__,
            layers_data=_data_layers,
            p4_x_coordinate=self.scenario.d_h * self.scenario.buiten_talud,
            profile_type=PipingWallReinforcementProfile,
        )
        return KoswatProfileBuilder.with_data(_builder_dict).build()
