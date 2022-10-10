from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)
from koswat.calculations.stability_wall.stability_wall_reinforcement_profile_calculation import (
    StabilityWallReinforcementProfileCalculation,
)


class TestStabilityWallReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = StabilityWallReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, StabilityWallReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)
