import math
from dataclasses import dataclass

from .road_class_protocol import (
    RoadClassProtocol,
)


@dataclass(kw_only=True)
class RoadClass47(RoadClassProtocol):
    key: str = "roads_class_47"
    polderside_name: str = "wegen_binnendijks_klasse47"
    waterside_name: str = "wegen_buitendijks_klasse47"
    is_polderside: bool = False
    width: float = math.nan
    adding_cost: float = math.nan
    removing_cost: float = math.nan

    def __hash__(self) -> int:
        return hash(self.key)
