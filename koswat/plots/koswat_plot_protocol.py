from typing import Any, Protocol, runtime_checkable

from matplotlib import pyplot


@runtime_checkable
class KoswatPlotProtocol(Protocol):
    koswat_object: Any
    subplot: pyplot.axes

    def plot(self, *args, **kwargs) -> pyplot.axes:
        """
        Plots a `koswat_object` into the provided plot `ax` with the requested `*args` and `**kwargs`.

        Returns:
            pyplot.axes: Canvas with plotted `koswat_object`.
        """
        pass
