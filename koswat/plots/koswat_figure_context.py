from __future__ import annotations

from matplotlib import pyplot
from matplotlib.figure import Figure


class KoswatFigureContext:
    _figure: Figure

    def __init__(self, dpi: int) -> None:
        self._figure = pyplot.figure(dpi=dpi)

    def __enter__(self) -> Figure:
        return self._figure

    def __exit__(self, *args, **kwargs) -> None:
        pyplot.close()
