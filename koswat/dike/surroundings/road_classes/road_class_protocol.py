from typing import ClassVar, Protocol, runtime_checkable


@runtime_checkable
class RoadClassProtocol(Protocol):
    class_name: ClassVar[str]

    is_polderside: bool
    width: float
    adding_costs: float
    removing_costs: float
