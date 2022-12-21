from shapefile import _Record
from shapely.geometry import Point

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class KoswatDikeLocationsShpFom(FileObjectModelProtocol):
    initial_point: Point
    end_point: Point
    record: _Record

    @property
    def dike_section(self) -> str:
        if not self.record:
            return ""
        try:
            return self.record.Dijksectie
        except Exception:
            return self.record.Sectie

    @property
    def dike_traject(self) -> str:
        if not self.record:
            return ""
        return self.record.Traject

    @property
    def dike_subtraject(self) -> str:
        if not self.record:
            return ""
        try:
            return self.record.Subtraject
        except Exception:
            return self.record.VAK

    def __init__(self) -> None:
        self.initial_point = None
        self.end_point = None
        self.record = None

    def is_valid(self) -> bool:
        if not self.initial_point or not self.end_point:
            return False
        return self.initial_point.is_valid and self.end_point.is_valid
