from dataclasses import dataclass


@dataclass(kw_only=True)
class BermCalculatorResult:
    """
    Result of the berm calculation.
    """

    berm_width: float
    berm_height: float
    slope: float
