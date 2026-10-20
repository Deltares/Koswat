from dataclasses import dataclass
from typing import ClassVar

from .infrastructure_type_protocol import (
    InfrastructureTypeProtocol,
)
from .road_class_base import RoadClassBase


@dataclass(eq=False)
class RoadClass7(RoadClassBase, InfrastructureTypeProtocol):
    infrastructure_name: ClassVar[str] = "roads_class_7"
    import_key: ClassVar[str] = "klasse7"
