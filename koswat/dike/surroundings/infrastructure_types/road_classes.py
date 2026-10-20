from dataclasses import dataclass
from typing import ClassVar

from .road_class_base import RoadClassBase


@dataclass(eq=False)
class RoadClass2(RoadClassBase):
    infrastructure_name: ClassVar[str] = "roads_class_2"
    import_key: ClassVar[str] = "klasse2"


@dataclass(eq=False)
class RoadClass7(RoadClassBase):
    infrastructure_name: ClassVar[str] = "roads_class_7"
    import_key: ClassVar[str] = "klasse7"


@dataclass(eq=False)
class RoadClass24(RoadClassBase):
    infrastructure_name: ClassVar[str] = "roads_class_24"
    import_key: ClassVar[str] = "klasse24"


@dataclass(eq=False)
class RoadClass47(RoadClassBase):
    infrastructure_name: ClassVar[str] = "roads_class_47"
    import_key: ClassVar[str] = "klasse47"


@dataclass(eq=False)
class RoadClassUnknown(RoadClassBase):
    infrastructure_name: ClassVar[str] = "roads_class_unknown"
    import_key: ClassVar[str] = "klasseunknown"
