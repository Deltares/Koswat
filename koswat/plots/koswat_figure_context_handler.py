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

    def __init__(self, output_path: Path, dpi: int) -> Figure:
        """
        Initializes the context setting up the path where the `Figure` (with resolution set by `dpi`) will be saved.

        Args:
            output_path (Path): Export location for the generated plot.
            dpi (int): Canvas resolution in dots-per-inch.

        Returns:
            Figure: Initialized instance from `pyplot.figure(dpi=dpi)`.
        """
        self._figure = pyplot.figure(dpi=dpi)
        self._output_path = output_path

    def __enter__(self) -> Figure:
        return self._figure

    def __exit__(self, *args, **kwargs) -> None:
        self._figure.savefig(self._output_path)
        pyplot.close()
