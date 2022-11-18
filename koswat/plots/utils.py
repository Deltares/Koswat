from __future__ import annotations

from pathlib import Path

from matplotlib import pyplot
from matplotlib.figure import Figure


def get_cmap(n_colors: int, name="hsv"):
    """
    Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.
    """
    return pyplot.cm.get_cmap(name, n_colors)

def get_plot(dpi: int) -> KoswatFigure:
    """
    Auxiliar method to reduce the direct imports of pyplot across the `Koswat` solution.

    Args:
        dpi (int): Resolution of the image (dots-per-inch).

    Returns:
        KoswatFigure: A wrapper arround `Figure` to easily save and close its stream.
    """
    return KoswatFigure(pyplot.figure(dpi=dpi))

class KoswatFigure:
    def __init__(self, fig: Figure) -> None:
        self._fig = fig
    def close(self):
        pyplot.close()
    def savefig(self, file_path: Path):
        self._fig.savefig(file_path)