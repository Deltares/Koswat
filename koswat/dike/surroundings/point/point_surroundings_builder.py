from shapely.geometry import Point

from koswat.core.protocols import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class PointSurroundingsBuilder(BuilderProtocol):
    point_surroundings_data: dict

    def __init__(self) -> None:
        self.point_surroundings_data = {}

    def build(self) -> PointSurroundings:
        _surroundings_matrix: dict[float, float] = self.point_surroundings_data.get(
            "surroundings_matrix", {}
        )

        return PointSurroundings(
            section=self.point_surroundings_data.get("section", ""),
            traject_order=self.point_surroundings_data.get("traject_order", -1),
            location=Point(self.point_surroundings_data["location"]),
            distance_to_surroundings_dict={
                _distance: _occurences
                for _distance, _occurences in sorted(_surroundings_matrix.items())
                if _occurences > 0
            },
        )
