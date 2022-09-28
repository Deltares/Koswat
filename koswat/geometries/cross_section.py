from __future__ import annotations

from typing import List, Optional, Protocol

from shapely.geometry.polygon import Polygon

from koswat.profiles.koswat_profile import KoswatProfile


class KoswatGeometry(Protocol):
    geometry: Polygon


class Layer(KoswatGeometry):
    geometry: Polygon


class CrossSection(KoswatGeometry):
    base_layer: Layer
    layers: Optional[List[Layer]]
    # TODO: This property  might fit better in the KoswatProfile itself.
    geometry: Polygon

    @classmethod
    def from_koswat_profile(cls, profile: KoswatProfile) -> CrossSection:
        _cs = cls()
        _geometry_points = []
        _geometry_points.extend(profile.points)
        _geometry_points.append(profile.points[0])
        _cs.geometry = Polygon(_geometry_points)
        return _cs
