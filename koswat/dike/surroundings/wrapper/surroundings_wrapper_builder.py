from __future__ import annotations

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside_builder import (
    KoswatBuildingsPoldersideBuilder,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


class SurroundingsWrapperBuilder(BuilderProtocol):
    buildings_foms: KoswatBuildingsPoldersideBuilder

    def __init__(self) -> None:
        self.buildings_foms = None

    def build(self) -> SurroundingsWrapper:
        _surroundings = SurroundingsWrapper()
        _surroundings.buldings_polderside = self.buildings_foms.build()
        return _surroundings

    @classmethod
    def from_files(cls, buildings_files: dict) -> SurroundingsWrapperBuilder:
        _builder = cls()
        _builder.buildings_foms = KoswatBuildingsPoldersideBuilder.from_files(
            buildings_files["csv_file"], buildings_files["shp_file"]
        )
        return _builder