from typing import Protocol, runtime_checkable


@runtime_checkable
class CostReportProtocol(Protocol):
    """
    A `Protocol` defining the properties of a report in Koswat.
    """

    total_cost: float
    total_cost_with_surtax: float
