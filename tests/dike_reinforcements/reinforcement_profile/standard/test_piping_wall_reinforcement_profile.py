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
from koswat.dike_reinforcements.reinforcement_profile.standard.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class TestPipingWallReinforcementProfile:
    def test_initialize(self):
        _profile = PipingWallReinforcementProfile()
        assert isinstance(_profile, PipingWallReinforcementProfile)
        assert isinstance(_profile, StandardReinforcementProfile)
        assert isinstance(_profile, ReinforcementProfileProtocol)
        assert isinstance(_profile, KoswatProfileProtocol)
        assert isinstance(_profile, KoswatProfileBase)

    @pytest.mark.parametrize(
        "allowed_waterside_reinforcement, expected_reinforcement_type",
        [
            pytest.param(
                True,
                PoldersideAndWatersideRoomCalculator,
                id="allow_waterside_reinforcement",
            ),
            pytest.param(
                False,
                PoldersideOnlyRoomCalculator,
                id="do_not_allow_waterside_reinforcement",
            ),
        ],
    )
    def test_when_get_reinforcement_room_calculator_given_waterside_reinforcement_then_returns_expected_calculator(
        self,
        allowed_waterside_reinforcement: bool,
        expected_reinforcement_type: Type[ReinforcementRoomCalculatorProtocol],
    ):

        # 1. Given
        _profile = PipingWallReinforcementProfile()
        _profile.characteristic_points = CharacteristicPoints(
            p_1=Point(-2.4, 0), p_8=Point(4.2, 0)
        )
        _profile.allow_waterside_reinforcement = allowed_waterside_reinforcement

        # 2. When
        _result_calculator = _profile.get_reinforcement_room_calculator()

        # 3. Then
        assert isinstance(_result_calculator, expected_reinforcement_type)
