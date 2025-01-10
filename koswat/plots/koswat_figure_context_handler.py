from __future__ import annotations

from pathlib import Path

from matplotlib import pyplot
from matplotlib.figure import Figure


class KoswatFigureContextHandler:
    """
    PyPlot fig context handler that opens the figure stream and closes it saving it to the appointed path.
    Usage example:
        with KoswatFigureContext(Path("C://my_plot.png"), 42) as _figure:
            _subplot = _figure.add_subplot()
            ...
    """

    def __init__(self, output_path: Path, dpi: int) -> None:
        """
        Initializes the context by invoking `pyplot.figure(dpi=dpi)` and saving its output to an internal field.

        Args:
            output_path (Path): Export location for the generated plot.
            dpi (int): Canvas resolution in dots-per-inch.

        """
        self._output_path = output_path
        self._dpi = dpi

    def __enter__(self) -> Figure:
        """
        Access to the context and invokation of `pyplot.figure(dpi)`.

        Returns:
            Figure: Initialized instance from `pyplot.figure(dpi=dpi)`."""
        self._figure = Figure(dpi=self._dpi)
        return self._figure

    def __exit__(self, *args, **kwargs) -> None:
        """
        Exit the current context and save the previously initialized `Figure`.
        """
        self._figure.savefig(self._output_path)
        pyplot.close(self._figure)
