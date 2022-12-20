from typing import Protocol, runtime_checkable

from shapely import geometry

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol


@runtime_checkable
class KoswatLayerBuilderProtocol(BuilderProtocol, Protocol):
    upper_linestring: geometry.LineString
    layer_data: dict

    def build(self) -> KoswatLayerProtocol:
        """
        Builds an instance of a `KoswatLayerProtocol` based on the provided `upper_linestring` and `layer_data`

        Returns:
            KoswatLayerProtocol: Valid instance of a `KoswatLayerProtocol`.
        """
        pass
