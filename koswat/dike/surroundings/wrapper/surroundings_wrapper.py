from typing import List

from shapely.geometry import Point

from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
)
from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)


class SurroundingsWrapper:
    traject: str
    buldings_polderside: KoswatBuildingsPolderside
    buildings_dikeside: KoswatSurroundingsProtocol

    platform_polderside: KoswatSurroundingsProtocol
    platform_dikeside: KoswatSurroundingsProtocol

    water_polderside: KoswatSurroundingsProtocol
    water_dikeside: KoswatSurroundingsProtocol

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
        self.buldings_polderside = None
        self.buildings_dikeside = None
        self.platform_polderside = None
        self.platform_dikeside = None
        self.water_polderside = None
        self.water_dikeside = None
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
    def locations(self) -> List[Point]:
        """
        Each location represents 1 meter in a real scale map.

        Returns:
            List[Point]: List of points along the polderside.
        """
        if not self.buldings_polderside:
            return []
        return [p.location for p in self.buldings_polderside.points]
