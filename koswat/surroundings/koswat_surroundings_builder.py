from __future__ import annotations

from koswat.builder_protocol import BuilderProtocol
from koswat.surroundings.koswat_buildings_polderside_builder import (
    KoswatBuildingsPoldersideBuilder,
)
from koswat.surroundings.koswat_surroundings import KoswatSurroundings


class KoswatSurroundingsBuilder(BuilderProtocol):
    buildings_foms: KoswatBuildingsPoldersideBuilder

    def __init__(self) -> None:
        self.buildings_foms = None

    def build(self) -> KoswatSurroundings:
        _surroundings = KoswatSurroundings()
        _surroundings.buldings_polderside = self.buildings_foms.build()
        return _surroundings

    @classmethod
    def from_files(cls, buildings_files: dict) -> KoswatSurroundingsBuilder:
        _builder = cls()
        _builder.buildings_foms = KoswatBuildingsPoldersideBuilder.from_files(
            buildings_files["csv_file"], buildings_files["shp_file"]
        )
        return _builder
