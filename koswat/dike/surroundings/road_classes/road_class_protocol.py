from typing import Protocol, runtime_checkable


@runtime_checkable
class RoadClassProtocol(Protocol):
    polderside_name: str
    waterside_name: str
    is_polderside: bool
    width: float
    adding_costs: float
    removing_costs: float

    @property
    def key(self) -> str:
        pass

    def __hash__(self) -> int:
        pass
