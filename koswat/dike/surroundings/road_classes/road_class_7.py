import math
from dataclasses import dataclass

from .road_class_base import RoadClassBase
from .road_class_protocol import (
    RoadClassProtocol,
)


@dataclass(kw_only=True, eq=False)
class RoadClass7(RoadClassBase, RoadClassProtocol):
    polderside_name: str = "wegen_binnendijks_klasse7"
    waterside_name: str = "wegen_buitendijks_klasse7"
    is_polderside: bool = False
    width: float = math.nan
    adding_costs: float = math.nan
    removing_costs: float = math.nan

    @property
    def key(self) -> str:
        return "roads_class_7"
