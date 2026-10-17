from typing import Protocol, runtime_checkable


@runtime_checkable
class RoadClassProtocol(Protocol):
    key: str
    polderside_name: str
    waterside_name: str
    is_polderside: bool
    width: float
    adding_cost: float
    removing_cost: float

    def __hash__(self) -> int:
        pass
