from __future__ import annotations

from typing import List, Optional, Protocol

from koswat.profiles.koswat_profile import KoswatProfile


class KoswatGeometry(Protocol):
    pass


class Layer(KoswatGeometry):
    pass


class CrossSection(KoswatGeometry):
    base_layer: Layer
    layers: Optional[List[Layer]]

    @classmethod
    def from_koswat_profile(cls, profile: KoswatProfile) -> CrossSection:
        pass
