from typing import Protocol


class CostReportProtocol(Protocol):
    total_cost: float
    total_volume: float

    def as_dict(self) -> float:
        pass
