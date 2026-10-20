from typing import Type

import pytest
from shapely import Point

from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.polderside_and_waterside_room_calculator import (
    PoldersideAndWatersideRoomCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.polderside_only_room_calculator import (
    PoldersideOnlyRoomCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_protocol import (
    ReinforcementRoomCalculatorProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_toe_reinforcement_profile import (
    StabilityWallToeReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class TestStabilityWallToeReinforcementProfile:
    def test_initialize(self):
        _profile = StabilityWallToeReinforcementProfile()
        assert isinstance(_profile, StabilityWallToeReinforcementProfile)
        assert isinstance(_profile, StandardReinforcementProfile)
        assert isinstance(_profile, ReinforcementProfileProtocol)
        assert isinstance(_profile, KoswatProfileProtocol)
        assert isinstance(_profile, KoswatProfileBase)

    def test_when_waterside_changed_then_returns_false(self):
        _profile = StabilityWallToeReinforcementProfile()
        assert _profile.waterside_changed is False

    @pytest.mark.parametrize(
        "allowed_waterside, expected_calculator",
        [
            (False, PoldersideOnlyRoomCalculator),
            (True, PoldersideAndWatersideRoomCalculator),
        ],
    )
    def test_when_get_reinforcement_room_calculator_then_returns_expected_calculator(
        self,
        allowed_waterside: bool,
        expected_calculator: Type[ReinforcementRoomCalculatorProtocol],
    ):

        # 1. Given
        _profile = StabilityWallToeReinforcementProfile()
        _profile.characteristic_points = CharacteristicPoints(
            p_1=Point(-2.4, 0), p_8=Point(4.2, 0)
        )

        # 2. When
        _result_calculator = _profile.get_reinforcement_room_calculator(
            waterside_allowed=allowed_waterside
        )

        # 3. Then
        assert isinstance(_result_calculator, expected_calculator)
