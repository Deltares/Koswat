import pytest

from koswat.calculations.reinforcement_profiles.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.reinforcement_profiles.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile_calculation import (
    CofferdamReinforcementProfileCalculation,
)
from koswat.calculations.reinforcement_profiles.outside_slope_reinforcement.outside_slope_reinforcement_profile_builder import (
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.calculations.reinforcement_profiles.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)


class TestOutsideSlopeReinforcementProfileBuilder:
    def test_initialize(self):
        _builder = OutsideSlopeReinforcementProfileBuilder()
        assert isinstance(_builder, OutsideSlopeReinforcementProfileBuilder)
        assert isinstance(_builder, ReinforcementProfileBuilderProtocol)

    def test_get_standard_reinforcement_calculator_raises_for_unknown_type(self):
        class MockClass:
            pass

        with pytest.raises(NotImplementedError):
            OutsideSlopeReinforcementProfileBuilder.get_standard_reinforcement_calculator(
                MockClass
            )

    def test_get_standard_reinforcement_calculator_returns_when_valid(self):
        _value = OutsideSlopeReinforcementProfileBuilder.get_standard_reinforcement_calculator(
            CofferdamReinforcementProfile
        )
        assert _value == CofferdamReinforcementProfileCalculation
