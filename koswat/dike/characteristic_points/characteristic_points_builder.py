import math
from typing import List

from shapely.geometry.point import Point

from koswat.core.protocols import BuilderProtocol
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


class CharacteristicPointsBuilder(BuilderProtocol):
    input_profile: KoswatInputProfileProtocol
    p4_x_coordinate: float

    def __init__(self) -> None:
        self.input_profile = None
        self.p4_x_coordinate = math.nan

    def _build_waterside(self, p4_x: float) -> List[Point]:
        _p4 = Point(p4_x, self.input_profile.kruin_hoogte)
        _p3_x = _p4.x - (
            (self.input_profile.kruin_hoogte - self.input_profile.buiten_berm_hoogte)
            * self.input_profile.buiten_talud
        )
        _p3 = Point(_p3_x, self.input_profile.buiten_berm_hoogte)
        _p2_x = _p3.x - self.input_profile.buiten_berm_breedte
        _p2 = Point(_p2_x, self.input_profile.buiten_berm_hoogte)
        _p1_x = _p2.x - (
            (self.input_profile.buiten_berm_hoogte - self.input_profile.buiten_maaiveld)
            * self.input_profile.buiten_talud
        )
        _p1 = Point(_p1_x, self.input_profile.buiten_maaiveld)
        return [_p1, _p2, _p3, _p4]

    def _build_polderside(self, p4_x: float) -> List[Point]:
        _x_p5 = p4_x + self.input_profile.kruin_breedte
        _p5 = Point(_x_p5, self.input_profile.kruin_hoogte)
        _x_p6 = _p5.x + (
            (self.input_profile.kruin_hoogte - self.input_profile.binnen_berm_hoogte)
            * self.input_profile.binnen_talud
        )
        _p6 = Point(_x_p6, self.input_profile.binnen_berm_hoogte)
        _x_p7 = _p6.x + self.input_profile.binnen_berm_breedte
        _p7 = Point(_x_p7, self.input_profile.binnen_berm_hoogte)
        _x_p8 = _p7.x + (
            (self.input_profile.binnen_berm_hoogte - self.input_profile.binnen_maaiveld)
            * self.input_profile.binnen_talud
        )
        _p8 = Point(_x_p8, self.input_profile.binnen_maaiveld)
        return [_p5, _p6, _p7, _p8]

    def build(self) -> CharacteristicPoints:
        if not self.input_profile:
            raise ValueError("Input Profile should be provided.")
        if math.isnan(self.p4_x_coordinate):
            self.p4_x_coordinate = 0

        _char_points = CharacteristicPoints()
        _char_points.waterside = self._build_waterside(self.p4_x_coordinate)
        _char_points.polderside = self._build_polderside(_char_points.p_4.x)
        return _char_points
