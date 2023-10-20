from abc import abstractmethod
import logging

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
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class ReinforcementProfileBuilderBase(ReinforcementProfileBuilderProtocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: type[StandardReinforcementProfile]

    @staticmethod
    def get_input_profile_calculator(
        reinforcement_type: type[StandardReinforcementProfile],
    ) -> ReinforcementInputProfileCalculationProtocol:
        raise NotImplementedError("Implement in concrete class.")

    @abstractmethod
    def _get_characteristic_points(
        self,
        input_profile: ReinforcementInputProfileProtocol,
    ) -> CharacteristicPoints:
        pass

    @abstractmethod
    def _get_reinforcement_layers_wrapper(
        self, profile_points: CharacteristicPoints
    ) -> ReinforcementLayersWrapper:
        pass

    def _get_reinforcement_profile_input(self) -> ReinforcementInputProfileProtocol:
        _calculator = self.get_input_profile_calculator(self.reinforcement_profile_type)
        _calculator.base_profile = self.base_profile
        _calculator.scenario = self.scenario
        return _calculator.build()

    def build(self) -> ReinforcementProfile:
        _profile = self.reinforcement_profile_type()
        logging.info(
            "Building reinforcement {}".format(
                _profile.input_data.reinforcement_domain_name
            )
        )

        _profile.old_profile = self.base_profile
        _profile.input_data = self._get_reinforcement_profile_input()
        _profile.characteristic_points = self._get_characteristic_points(
            _profile.input_data
        )
        _profile.layers_wrapper = self._get_reinforcement_layers_wrapper(
            _profile.characteristic_points
        )
        logging.info(
            "Generated reinforcement {}".format(
                _profile.input_data.reinforcement_domain_name
            )
        )

        return _profile
