from typing import List

from shapely.geometry import Point

from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
)


class SurroundingsWrapper:
    buldings_polderside: KoswatBuildingsPolderside

    def __init__(self) -> None:
        self.buldings_polderside = None

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
