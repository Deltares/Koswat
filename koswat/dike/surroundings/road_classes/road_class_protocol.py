from typing import ClassVar, Protocol, runtime_checkable


@runtime_checkable
class RoadClassProtocol(Protocol):
    class_name: ClassVar[str]
    import_key: ClassVar[str]

    is_polderside: bool
    width: float
    adding_costs: float
    removing_costs: float

    @classmethod
    def get_polderside_source_name(cls) -> str:
        pass

    @classmethod
    def get_waterside_source_name(cls) -> str:
        pass

    def __hash__(self) -> int:
        pass
