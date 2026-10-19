import math
from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from .road_class_protocol import RoadClassProtocol


@dataclass
class RoadClassBase(ABC, RoadClassProtocol):
    class_name: ClassVar[str]
    import_key: ClassVar[str]

    is_polderside: bool = False
    width: float = math.nan
    adding_costs: float = math.nan
    removing_costs: float = math.nan

    @classmethod
    def get_polderside_source_name(cls) -> str:
        return f"wegen_binnendijks_{cls.import_key}"

    @classmethod
    def get_waterside_source_name(cls) -> str:
        return f"wegen_buitendijks_{cls.import_key}"

    def __hash__(self) -> int:
        return hash(self.class_name)
