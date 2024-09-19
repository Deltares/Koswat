import pytest

from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile_calculation import (
    CofferdamInputProfileCalculation,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.outside_slope_reinforcement_profile_builder import (
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)


class TestOutsideSlopeReinforcementProfileBuilder:
    def test_initialize(self):
        _builder = OutsideSlopeReinforcementProfileBuilder()
        assert isinstance(_builder, OutsideSlopeReinforcementProfileBuilder)
        assert isinstance(_builder, ReinforcementProfileBuilderProtocol)

    def test_get_outside_slope_reinforcement_calculator_raises_for_unknown_type(self):
        class MockClass:
            pass

        with pytest.raises(NotImplementedError):
            OutsideSlopeReinforcementProfileBuilder.get_input_profile_calculator(
                MockClass
            )

    def test_get_standard_reinforcement_calculator_returns_when_valid(self):
        _value = OutsideSlopeReinforcementProfileBuilder.get_input_profile_calculator(
            CofferdamReinforcementProfile
        )
        assert isinstance(_value, CofferdamInputProfileCalculation)
