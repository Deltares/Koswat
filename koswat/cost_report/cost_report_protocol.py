from typing import Protocol, runtime_checkable


@runtime_checkable
class CostReportProtocol(Protocol):
    total_cost: float
    total_volume: float
