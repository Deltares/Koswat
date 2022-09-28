from __future__ import annotations

from typing import List, Protocol

from shapely.geometry.point import Point

from koswat.profiles.koswat_input_profile import KoswatInputProfile


class SideProtocol(Protocol):
    points: List[Point]

    @classmethod
    def from_input_profile(cls, input_profile: KoswatInputProfile) -> SideProtocol:
        pass
