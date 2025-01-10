from __future__ import annotations

from typing import List, Protocol

from shapely import geometry

from koswat.core.protocols import BuilderProtocol
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper import (
    KoswatLayersWrapperProtocol,
)


class KoswatLayersWrapperBuilderProtocol(BuilderProtocol, Protocol):
    layers_data: dict
    profile_points: List[geometry.Point]

    def build(self) -> KoswatLayersWrapperProtocol:
        """
        Builds an instance of `KoswatLayersWrapperProtocol` based on the class required fields `layers_data` and `profile_points`.

        Returns:
            KoswatLayersWrapperProtocol: Valid initialized instance of a `KoswatLayersWrapperProtocol`.
        """
        pass
