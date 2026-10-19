from dataclasses import dataclass
from typing import ClassVar

from .road_class_base import RoadClassBase
from .road_class_protocol import (
    RoadClassProtocol,
)


@dataclass(eq=False)
class RoadClass2(RoadClassBase, RoadClassProtocol):
    class_name: ClassVar[str] = "roads_class_2"
    import_key: ClassVar[str] = "klasse2"
