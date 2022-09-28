from __future__ import annotations

from typing import List

from shapely.geometry.point import Point

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.side_protocol import SideProtocol


class Waterside(SideProtocol):
    p_1: Point
    p_2: Point
    p_3: Point
    p_4: Point

    def __init__(self) -> None:
        self.p_1 = None
        self.p_2 = None
        self.p_3 = None
        self.p_4 = None

    @property
    def points(self) -> List[Point]:
        return [
            self.p_1,
            self.p_2,
            self.p_3,
            self.p_4,
        ]

    @classmethod
    def from_input_profile(cls, input_profile: KoswatInputProfile) -> Waterside:
        _waterside = cls()
        _p4_x = 0
        _waterside.p_4 = Point(_p4_x, input_profile.kruin_hoogte)
        _p3_x = _p4_x - (
            (input_profile.kruin_hoogte - input_profile.buiten_berm_hoogte)
            * input_profile.buiten_talud
        )
        _waterside.p_3 = Point(_p3_x, input_profile.buiten_berm_hoogte)
        _p2_x = _p3_x - input_profile.buiten_berm_breedte
        _waterside.p_2 = Point(_p2_x, input_profile.buiten_berm_hoogte)
        _p1_x = _p2_x - (
            (input_profile.buiten_berm_hoogte - input_profile.buiten_maaiveld)
            * input_profile.buiten_talud
        )
        _waterside.p_1 = Point(_p1_x, input_profile.buiten_maaiveld)
        return _waterside
