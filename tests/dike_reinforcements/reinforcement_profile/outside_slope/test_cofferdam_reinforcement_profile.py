import pytest

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.surroundings.point import PointObstacleSurroundings
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferdamInputProfile,
)
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

    @pytest.mark.parametrize(
        "waterside_slope, expected",
        [
            pytest.param(1.0, False, id="No change"),
            pytest.param(0.5, True, id="Reduced slope"),
            pytest.param(1.5, True, id="Increased slope"),
        ],
    )
    def test_when_waterside_changed_given_slope_returns_expected(
        self, waterside_slope: float, expected: bool
    ):
        # 1. Given
        _profile = CofferdamReinforcementProfile()
        _profile.input_data = CofferdamInputProfile(waterside_slope=waterside_slope)
        _profile.old_profile = KoswatProfileBase()
        _profile.old_profile.input_data = CofferdamInputProfile(waterside_slope=1.0)

        # 2. When
        _changed = _profile.waterside_changed

        # 3. Then
        assert _changed == expected

    @pytest.mark.parametrize("allow_waterside", [True, False])
    def test_when_get_reinforcement_room_calculator_given_point_obstacle_location_then_calculator_returns_true(
        self, allow_waterside: bool
    ):
        # 1. Given
        _profile = CofferdamReinforcementProfile()
        _point_obstacle_location = (
            PointObstacleSurroundings()
        )  # The point obstacle location is not relevant for the cofferdam room calculator

        # 2. When
        _calculator = _profile.get_reinforcement_room_calculator(
            waterside_allowed=allow_waterside
        )

        # 3. Then
        assert isinstance(_calculator, ReinforcementRoomCalculatorProtocol)
        assert _calculator.reinforcement_has_room(_point_obstacle_location) == True
