from koswat.dike_reinforcements.reinforcement_profiles.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profiles.outside_slope_reinforcement.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)


class TestCofferDamReinforcementProfile:
    def test_initialize(self):
        _profile = CofferdamReinforcementProfile()
        assert isinstance(_profile, CofferdamReinforcementProfile)
        assert isinstance(_profile, OutsideSlopeReinforcementProfile)
        assert str(_profile) == "Kistdam"
