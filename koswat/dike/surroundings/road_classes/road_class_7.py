from dataclasses import dataclass
from typing import ClassVar

from .road_class_base import RoadClassBase
from .road_class_protocol import (
    RoadClassProtocol,
)


@dataclass(kw_only=True, eq=False)
class RoadClass7(RoadClassBase, RoadClassProtocol):
    import_key: ClassVar[str] = "klasse7"

    @property
    def class_name(self) -> str:
        return "roads_class_7"
