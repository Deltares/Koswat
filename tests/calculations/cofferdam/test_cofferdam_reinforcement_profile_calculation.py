from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.cofferdam.cofferdam_reinforcement_profile_calculation import (
    CofferdamReinforcementProfileCalculation,
)
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)


class TestCofferDamReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = CofferdamReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, CofferdamReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)
