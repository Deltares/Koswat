from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.surroundings.point import PointObstacleSurroundings
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_protocol import (
    ReinforcementRoomCalculatorProtocol,
)


class TestCofferDamReinforcementProfile:
    def test_initialize(self):
        _profile = CofferdamReinforcementProfile()
        assert isinstance(_profile, CofferdamReinforcementProfile)
        assert isinstance(_profile, OutsideSlopeReinforcementProfile)
        assert isinstance(_profile, ReinforcementProfileProtocol)
        assert isinstance(_profile, KoswatProfileProtocol)
        assert isinstance(_profile, KoswatProfileBase)

    def test_when_get_polderside_reinforcement_calculator_given_point_obstacle_location_then_calculator_returns_true(
        self,
    ):
        # 1. Given
        _profile = CofferdamReinforcementProfile()
        _point_obstacle_location = (
            PointObstacleSurroundings()
        )  # The point obstacle location is not relevant for the cofferdam room calculator

        # 2. When
        _calculator = _profile.get_polderside_reinforcement_calculator()

        # 3. Then
        assert isinstance(_calculator, ReinforcementRoomCalculatorProtocol)
        assert _calculator.reinforcement_has_room(_point_obstacle_location) == True

    def test_when_get_waterside_reinforcement_calculator_given_point_obstacle_location_then_calculator_returns_true(
        self,
    ):
        # 1. Given
        _profile = CofferdamReinforcementProfile()
        _point_obstacle_location = (
            PointObstacleSurroundings()
        )  # The point obstacle location is not relevant for the cofferdam room calculator

        # 2. When
        _calculator = _profile.get_waterside_reinforcement_calculator()

        # 3. Then
        assert isinstance(_calculator, ReinforcementRoomCalculatorProtocol)
        assert _calculator.reinforcement_has_room(_point_obstacle_location) == True
