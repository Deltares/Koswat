from dataclasses import dataclass
from typing import ClassVar

from .road_class_base import RoadClassBase
from .road_class_protocol import RoadClassProtocol


@dataclass(eq=False)
class RoadClass47(RoadClassBase, RoadClassProtocol):
    class_name: ClassVar[str] = "roads_class_47"
    import_key: ClassVar[str] = "klasse47"
