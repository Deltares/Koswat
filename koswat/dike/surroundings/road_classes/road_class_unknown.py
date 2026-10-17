import math
from dataclasses import dataclass

from .road_class_protocol import (
    RoadClassProtocol,
)


@dataclass(kw_only=True)
class RoadClassUnknown(RoadClassProtocol):
    key: str = "roads_class_unknown"
    polderside_name: str = "wegen_binnendijks_klasseonbekend"
    waterside_name: str = "wegen_buitendijks_klasseonbekend"
    is_polderside: bool = False
    width: float = math.nan
    adding_cost: float = math.nan
    removing_cost: float = math.nan

    def __hash__(self) -> int:
        return hash(self.key)
