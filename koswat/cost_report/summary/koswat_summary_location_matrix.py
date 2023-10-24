from dataclasses import dataclass, field
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
)


@dataclass
class KoswatLocationReinforcements:
    location: PointSurroundings
    reinforcement_list: list[ReinforcementProfile] = field(default_factory=lambda: [])


class KoswatSummaryLocationMatrix:
    locations_matrix: list[KoswatLocationReinforcements]

    def __init__(self) -> None:
        self.locations_matrix = []

    def __add__(self, other):
        return other + self

    @classmethod
    def from_point_surroundings_list(cls, point_surroundings: list[PointSurroundings]):
        _this_cls = cls()
        _this_cls.locations_matrix = list(
            map(lambda x: KoswatLocationReinforcements(location=x), point_surroundings)
        )
        return _this_cls
