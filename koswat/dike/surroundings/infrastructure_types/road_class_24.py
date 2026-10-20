from dataclasses import dataclass
from typing import ClassVar

from .infrastructure_type_protocol import (
    InfrastructureTypeProtocol,
)
from .road_class_base import RoadClassBase


@dataclass(eq=False)
class RoadClass24(RoadClassBase, InfrastructureTypeProtocol):
    infrastructure_name: ClassVar[str] = "roads_class_24"
    import_key: ClassVar[str] = "klasse24"
