import logging

from shapely.geometry import Point

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside import (
    KoswatSurroundingsPolderside,
)


class SurroundingsWrapper:
    dike_section: str
    traject: str
    subtraject: str
    apply_waterside: bool
    apply_buildings: bool
    apply_railways: bool
    apply_waters: bool

    buildings_polderside: KoswatSurroundingsPolderside
    buildings_dikeside: KoswatSurroundingsProtocol

    railways_polderside: KoswatSurroundingsPolderside
    railways_dikeside: KoswatSurroundingsProtocol

    waters_polderside: KoswatSurroundingsPolderside
    waters_dikeside: KoswatSurroundingsProtocol

    roads_class_2_polderside: KoswatSurroundingsProtocol
    roads_class_7_polderside: KoswatSurroundingsProtocol
    roads_class_24_polderside: KoswatSurroundingsProtocol
    roads_class_47_polderside: KoswatSurroundingsProtocol
    roads_class_unknown_polderside: KoswatSurroundingsProtocol

    roads_class_2_dikeside: KoswatSurroundingsProtocol
    roads_class_7_dikeside: KoswatSurroundingsProtocol
    roads_class_24_dikeside: KoswatSurroundingsProtocol
    roads_class_47_dikeside: KoswatSurroundingsProtocol
    roads_class_unknown_dikeside: KoswatSurroundingsProtocol

    def __init__(self) -> None:
        self.dike_section = ""
        self.traject = ""
        self.subtraject = ""
        
        self.apply_waterside = None
        self.apply_buildings = None
        self.apply_railways = None
        self.apply_waters = None

        self.buildings_polderside = None
        self.buildings_dikeside = None
        self.railways_polderside = None
        self.railways_dikeside = None
        self.waters_polderside = None
        self.waters_dikeside = None
        self.roads_class_2_polderside = None
        self.roads_class_7_polderside = None
        self.roads_class_24_polderside = None
        self.roads_class_47_polderside = None
        self.roads_class_unknown_polderside = None
        self.roads_class_2_dikeside = None
        self.roads_class_7_dikeside = None
        self.roads_class_24_dikeside = None
        self.roads_class_47_dikeside = None
        self.roads_class_unknown_dikeside = None

    @property
    def locations(self) -> list[PointSurroundings]:
        """
        Overlay of locations of the different surroundings that are present.
        Each location represents 1 meter in a real scale map.

        Returns:
            List[PointSurroundings]: List of points along the polderside.
        """
        if not self.buildings_polderside:
            return []
        
        _points = self.buildings_polderside.points
            
        for _p, _point in enumerate(self.buildings_polderside.points):
            
            if not self.apply_buildings:
                _points[_p].distance_to_surroundings = []
                
            if self.apply_railways and self.railways_polderside:
                if (not _point.location == self.railways_polderside.points[_p].location):
                    logging.warning(f"Mismatching railway polderside location {self.railways_polderside.points[_p].location}")
                _points[_p].distance_to_surroundings += self.railways_polderside.points[_p].distance_to_surroundings
                
            if self.apply_waters and self.waters_polderside:
                if (not _point.location == self.waters_polderside.points[_p].location):
                    logging.warning(f"Mismatching water polderside location {self.waters_polderside.points[_p].location}")
                _points[_p].distance_to_surroundings += self.waters_polderside.points[_p].distance_to_surroundings
                
        return _points
    
    def get_locations_after_distance(self, distance: float) -> list[Point]:
        """
        Gets all locations which are safe from surroundings (building/railway/water) in a radius of `distance`.

        Args:
            distance (float): Radius from each point that should be free of surroundings.

        Returns:
            List[Point]: List of safe locations (points).
        """

        def is_at_safe_distance(point_surroundings: PointSurroundings) -> bool:
            if not point_surroundings.distance_to_surroundings:
                return True
            return distance < point_surroundings.distance_to_surroundings[0]

        return list(filter(is_at_safe_distance, self.locations))
