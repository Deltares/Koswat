from typing import Protocol

from shapely import geometry
from typing_extensions import runtime_checkable

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol


@runtime_checkable
class KoswatLayerBuilderProtocol(BuilderProtocol, Protocol):
    upper_linestring: geometry.LineString
    layer_data: dict

    def build(self) -> KoswatLayerProtocol:
        pass
