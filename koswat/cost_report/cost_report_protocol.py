from typing import Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class CostReportProtocol(Protocol):
    total_cost: float
    total_volume: float
