from __future__ import annotations
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
)


class KoswatSummaryLocationMatrix:
    locations_matrix: dict[PointSurroundings, list[ReinforcementProfile]]

    def __init__(self) -> None:
        self.locations_matrix = []

    @classmethod
    def from_point_surroundings_list(cls, point_surroundings: list[PointSurroundings]):
        _this_cls = cls()
        _this_cls.locations_matrix = dict((_ps, []) for _ps in point_surroundings)
        return _this_cls
