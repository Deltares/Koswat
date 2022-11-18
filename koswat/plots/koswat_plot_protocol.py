from typing import Any, Protocol

from matplotlib import pyplot
from typing_extensions import runtime_checkable


@runtime_checkable
class KoswatPlotProtocol(Protocol):
    koswat_object: Any

    def plot(self, subplot: pyplot.axes, *args, **kwargs) -> pyplot.axes:
        """
        Plots a `koswat_object` into the provided plot `ax` with the requested `*args` and `**kwargs`.

        Args:
            subplot (pyplot.axes): Pyplot containing the drawing canvas.
        """
        pass
