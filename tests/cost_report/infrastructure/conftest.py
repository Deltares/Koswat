import math
from dataclasses import dataclass
from typing import Callable, Iterable

import pytest
from shapely import Point

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


@pytest.fixture(name="reinforcement_profile_builder")
def _get_dummy_reinforcment_profile_builder() -> Iterable[
    Callable[[CharacteristicPoints, CharacteristicPoints], ReinforcementProfileProtocol]
]:
    @dataclass
    class DummyReinforcementProfile(KoswatProfileBase, ReinforcementProfileProtocol):
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
