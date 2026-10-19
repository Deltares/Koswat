import math
from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from .road_class_protocol import RoadClassProtocol


@dataclass
class RoadClassBase(ABC, RoadClassProtocol):
    class_name: ClassVar[str] = ""
    import_key: ClassVar[str] = ""

    imported_name: str = ""

    width: float = math.nan
    adding_costs: float = math.nan
    removing_costs: float = math.nan

    @classmethod
    def get_polderside_source_name(cls) -> str:
        return f"wegen_binnendijks_{cls.import_key}"

    @classmethod
    def get_waterside_source_name(cls) -> str:
        return f"wegen_buitendijks_{cls.import_key}"

    @property
    def is_polderside(self) -> bool:
        return self.imported_name == self.__class__.get_polderside_source_name()

    def __hash__(self) -> int:
        return hash(self.class_name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, RoadClassBase):
            return False
        return self.class_name == other.class_name
