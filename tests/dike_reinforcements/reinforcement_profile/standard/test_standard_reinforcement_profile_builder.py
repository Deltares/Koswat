import pytest

from koswat.dike_reinforcements.input_profile import (
    PipingWallInputProfileCalculation,
    SoilInputProfileCalculation,
    StabilityWallInputProfileCalculation,
    VPSInputProfileCalculation,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile import (
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
    VPSReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile_builder import (
    StandardReinforcementProfileBuilder,
)


class TestStandardReinforcementProfileBuilder:
    def test_initialize(self):
        _builder = StandardReinforcementProfileBuilder()
        assert isinstance(_builder, StandardReinforcementProfileBuilder)
        assert isinstance(_builder, ReinforcementProfileBuilderProtocol)

    def test_get_standard_reinforcement_calculator_raises_for_unknown_type(self):
        class MockClass(StandardReinforcementProfile):
            pass

        assert issubclass(MockClass, StandardReinforcementProfile)
        with pytest.raises(NotImplementedError):
            StandardReinforcementProfileBuilder.get_input_profile_calculator(MockClass)

    @pytest.mark.parametrize(
        "reinforcement_profile_type, expected_calculator",
        [
            pytest.param(
                SoilReinforcementProfile,
                SoilInputProfileCalculation,
                id="[Standard] Soil reinforcement",
            ),
            pytest.param(
                VPSReinforcementProfile,
                VPSInputProfileCalculation,
                id="[Standard] VPS reinforcement",
            ),
            pytest.param(
                PipingWallReinforcementProfile,
                PipingWallInputProfileCalculation,
                id="[Standard] Piping wall reinforcement",
            ),
            pytest.param(
                StabilityWallReinforcementProfile,
                StabilityWallInputProfileCalculation,
                id="[Standard] Stability wall reinforcement",
            ),
        ],
    )
    def test_get_standard_reinforcement_calculator_returns_when_valid(
        self,
        reinforcement_profile_type: type[StandardReinforcementProfile],
        expected_calculator: ReinforcementInputProfileCalculationProtocol,
    ):
        _calculator = StandardReinforcementProfileBuilder.get_input_profile_calculator(
            reinforcement_profile_type
        )
        assert isinstance(_calculator, ReinforcementInputProfileCalculationProtocol)
        assert isinstance(_calculator, expected_calculator)
