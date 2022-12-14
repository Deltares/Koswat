from typing import List

from shapefile import _Record
from shapely.geometry import Point

from koswat.io.shp.koswat_shp_fom_protocol import KoswatShpFomProtocol


class KoswatDikeLocationsShpFom(KoswatShpFomProtocol):
    initial_point: Point
    end_point: Point
    record: _Record

    def __init__(self) -> None:
        self.initial_point = None
        self.end_point = None
        self.record = None

    def is_valid(self) -> bool:
        if not self.initial_point or not self.end_point:
            return False
        return self.initial_point.is_valid and self.end_point.is_valid


class KoswatDikeLocationsWrapperShpFom(KoswatShpFomProtocol):
    dike_locations_shp_fom: List[KoswatDikeLocationsShpFom]

    def __init__(self) -> None:
        self.dike_locations_shp_fom = []
    
    def get_by_section(self, section: str) ->List[KoswatDikeLocationsShpFom]:
        return list(filter(lambda x: x.record.Dijksectie.lower() == section.lower(), self.dike_locations_shp_fom))

