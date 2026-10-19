from dataclasses import dataclass
from typing import ClassVar

from .road_class_base import RoadClassBase
from .road_class_protocol import (
    RoadClassProtocol,
)


@dataclass(kw_only=True, eq=False)
class RoadClass24(RoadClassBase, RoadClassProtocol):
    class_name: ClassVar[str] = "roads_class_24"
    import_key: ClassVar[str] = "klasse24"
