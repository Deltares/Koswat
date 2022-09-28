from __future__ import annotations

from typing import List

from shapely.geometry.point import Point

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.side_protocol import SideProtocol


class Polderside(SideProtocol):
    p_5: Point
    p_6: Point
    p_7: Point
    p_8: Point

    @property
    def points(self) -> List[Point]:
        return [
            self.p_5,
            self.p_6,
            self.p_7,
            self.p_8,
        ]

    @classmethod
    def from_input_profile(cls, input_profile: KoswatInputProfile) -> Polderside:
        _polderside = cls()
        _x_p4 = 0
        _x_p5 = _x_p4 + input_profile.kruin_breedte
        _polderside.p_5 = Point(_x_p5, input_profile.kruin_hoogte)
        _x_p6 = _x_p5 + (
            (input_profile.kruin_hoogte - input_profile.binnen_berm_hoogte)
            * input_profile.binnen_talud
        )
        _polderside.p_6 = Point(_x_p6, input_profile.binnen_berm_hoogte)
        _x_p7 = _x_p6 + input_profile.binnen_berm_breedte
        _polderside.p_7 = Point(_x_p7, input_profile.binnen_berm_hoogte)
        _x_p8 = _x_p7 + (
            (input_profile.binnen_berm_hoogte - input_profile.binnen_maaiveld)
            * input_profile.binnen_talud
        )
        _polderside.p_8 = Point(_x_p8, input_profile.binnen_maaiveld)

        return _polderside
