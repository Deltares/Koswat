from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class PointSurroundingsBuilder(BuilderProtocol):
    point_surroundings_data: dict

    def __init__(self) -> None:
        self.point_surroundings_data = {}

    def build(self) -> PointSurroundings:
        _point = PointSurroundings()
        _point.section = self.point_surroundings_data.get("section", "")
        _point.traject_order = self.point_surroundings_data.get("traject_order", -1)
        _point.location = Point(self.point_surroundings_data["location"])
        _point.distance_to_buildings = self.point_surroundings_data.get(
            "distance_to_buildings", []
        )
        return _point
