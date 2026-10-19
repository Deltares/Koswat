from dataclasses import dataclass
from typing import ClassVar

from .road_class_base import RoadClassBase
from .road_class_protocol import (
    RoadClassProtocol,
)


@dataclass(eq=False)
class RoadClass7(RoadClassBase, RoadClassProtocol):
    class_name: ClassVar[str] = "roads_class_7"
    import_key: ClassVar[str] = "klasse7"
