from __future__ import annotations

from typing import List, Protocol

from shapely import geometry

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper import (
    KoswatLayersWrapperProtocol,
)


class KoswatLayersWrapperBuilderProtocol(BuilderProtocol, Protocol):
    layers_data: dict
    profile_points: List[geometry.Point]

    def build(self) -> KoswatLayersWrapperProtocol:
        pass
