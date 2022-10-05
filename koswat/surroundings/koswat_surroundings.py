from typing import Any, List

from shapely.geometry import Point

from koswat.surroundings.koswat_buildings_polderside import KoswatBuildingsPolderside


class KoswatSurroundings:
    buldings_polderside: KoswatBuildingsPolderside = None

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
