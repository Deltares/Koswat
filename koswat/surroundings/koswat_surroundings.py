from typing import List

from shapely.geometry import Point

from koswat.surroundings.koswat_buildings_polderside import KoswatBuildingsPolderside


class KoswatSurroundings:
    buldings_polderside: KoswatBuildingsPolderside = None

    @property
    def locations(self) -> List[Point]:
        if not self.buldings_polderside:
            return []
        return [p.location for p in self.buldings_polderside.points]
