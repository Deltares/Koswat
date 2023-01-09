from typing import Protocol, runtime_checkable


@runtime_checkable
class CostReportProtocol(Protocol):
    """
    A `Protocol` defining the properties of a report in Koswawt.
    """

    total_cost: float
    total_volume: float
