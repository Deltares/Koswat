import copy
import math
from dataclasses import dataclass
from typing import Callable, Iterable

import pytest
from shapely import Point

from koswat.cost_report.infrastructure.profile_zone_calculator import (
    ProfileZoneCalculator,
)
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)

_waterside_reinforced_points = [(-18, 0), (-18, 0), (-18, 0)]


class TestProfileZoneCalculator:
    def test_initialize(self):
        # 1. Define test data.
        _calculator = ProfileZoneCalculator(reinforced_profile=None)

        # 2. Verify expectations.
        assert isinstance(_calculator, ProfileZoneCalculator)
        assert not _calculator.reinforced_profile
        assert _calculator.calculate() == (math.nan, math.nan)

    @pytest.fixture(name="reinforcement_profile_builder")
    def _get_dummy_reinforcment_profile_builder(
        self,
    ) -> Iterable[
        Callable[
            [CharacteristicPoints, CharacteristicPoints], ReinforcementProfileProtocol
        ]
    ]:
        @dataclass
        class DummyReinforcementProfile(
            KoswatProfileBase, ReinforcementProfileProtocol
        ):
            output_name: str = "Dummy reinforcement"
            input_data: ReinforcementInputProfileProtocol = None
            layers_wrapper: ReinforcementLayersWrapper = None
            old_profile: KoswatProfileProtocol = None
            new_ground_level_surface: float = math.nan

        def assign_char_points(point_list: list[tuple[float]]) -> CharacteristicPoints:
            return CharacteristicPoints(
                p_1=Point(point_list[0]),
                p_2=Point(point_list[1]),
                p_3=Point(point_list[2]),
                p_4=Point(point_list[3]),
                p_5=Point(point_list[4]),
                p_6=Point(point_list[5]),
                p_7=Point(point_list[6]),
                p_8=Point(point_list[7]),
            )

        def reinforcement_profile_builder(
            base_points: list[tuple[float]],
            reinforcment_points: list[tuple[float]],
        ) -> ReinforcementProfileProtocol:
            return DummyReinforcementProfile(
                characteristic_points=assign_char_points(reinforcment_points),
                old_profile=KoswatProfileBase(
                    characteristic_points=assign_char_points(base_points)
                ),
            )

        yield reinforcement_profile_builder

    @pytest.mark.parametrize(
        "points_reinforcement, expected_zones",
        [
            # Without dh0 increase, we expect zone a and zone b calculated.
            pytest.param(
                _waterside_reinforced_points
                + [(0, 6), (10, 6), (39.7, -0.6), (67.7, -0.6), (74, -2)],
                (10, 64),
                id="Without dh0 increase - Soil reinforcement",
            ),
            pytest.param(
                _waterside_reinforced_points
                + [(0, 6), (10, 6), (43.74, -1.5), (53.75, -1.5), (56, -2)],
                (10, 46),
                id="Without dh0 increase - Vertical Piping Solution",
            ),
            pytest.param(
                _waterside_reinforced_points
                + [(0, 6), (10, 6), (46, -2), (46, -2), (46, -2)],
                (10, 36),
                id="Without dh0 increase - Piping Wall reinforcement",
            ),
            pytest.param(
                _waterside_reinforced_points
                + [(0, 6), (10, 6), (34, -2), (34, -2), (34, -2)],
                (10, 24),
                id="Without dh0 increase - Stability Wall reinforcement",
            ),
            pytest.param(
                _waterside_reinforced_points
                + [(0, 6), (10, 6), (34, -2), (34, -2), (34, -2)],
                (10, 24),
                id="Without dh0 increase - Cofferdam reinforcement",
            ),
            # With dh0 increase (of 1), we expect only zone b calculated.
            pytest.param(
                _waterside_reinforced_points
                + [(3, 7), (13, 7), (40.87, -0.6), (68.87, -0.6), (74, -2)],
                (math.nan, 71),
                id="With dh0 increase to 1 - Soil reinforcement",
            ),
            pytest.param(
                _waterside_reinforced_points
                + [(3, 7), (13, 7), (44.17, -1.5), (54.17, -1.5), (56, -2)],
                (math.nan, 53),
                id="With dh0 increase to 1 - Vertical Piping Solution",
            ),
            pytest.param(
                _waterside_reinforced_points
                + [(3, 7), (13, 7), (46, -2), (46, -2), (46, -2)],
                (math.nan, 43),
                id="With dh0 increase to 1 - Piping Wall reinforcement",
            ),
            pytest.param(
                _waterside_reinforced_points
                + [(3, 7), (13, 7), (34, -2), (34, -2), (34, -2)],
                (math.nan, 31),
                id="With dh0 increase to 1 - Stability Wall reinforcement",
            ),
            pytest.param(
                _waterside_reinforced_points
                + [(0, 7), (10, 7), (34, -2), (34, -2), (34, -2)],
                (math.nan, 34),
                id="With dh0 increase to 1- Cofferdam reinforcement",
            ),
        ],
    )
    def test_given_reinforcement_profile_when_calculate_then_expected_zones(
        self,
        points_reinforcement: list[tuple[float]],
        expected_zones: tuple[float, float],
        reinforcement_profile_builder: Callable[
            [list[tuple[float]], list[tuple[float]]], ReinforcementProfileProtocol
        ],
    ):
        # 1. Define test data.
        _points_base_profile = [
            (-18, 0),
            (-18, 0),
            (-18, 0),
            (0, 6),
            (10, 6),
            (34, -2),
            (34, -2),
            (34, -2),
        ]
        _reinforcement_profile = reinforcement_profile_builder(
            _points_base_profile, points_reinforcement
        )
        assert isinstance(_reinforcement_profile, ReinforcementProfileProtocol)

        # 2. Run test.
        _result_zones = ProfileZoneCalculator(
            reinforced_profile=_reinforcement_profile
        ).calculate()

        # 3. Verify expectations.
        assert _result_zones == pytest.approx(expected_zones)
