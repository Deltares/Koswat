from shapely.geometry import Point

from koswat.io.shp.koswat_shp_fom_protocol import KoswatShpFomProtocol


class KoswatDikeLocationsShpFom(KoswatShpFomProtocol):
    initial_point: Point
    end_point: Point

    def __init__(self) -> None:
        self.initial_point = None
        self.end_point = None

    def is_valid(self) -> bool:
        if not self.initial_point or not self.end_point:
            return False
        return self.initial_point.is_valid and self.end_point.is_valid