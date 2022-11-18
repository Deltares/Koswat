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


def get_plot(dpi: int) -> Figure:
    """
    Auxiliar method to reduce the direct imports of pyplot across the `Koswat` solution.

    Args:
        dpi (int): Resolution of the image (dots-per-inch).

    Returns:
        Figure: The canvas generated from pyplot.
    """
    return pyplot.figure(dpi=dpi)


def close_figure():
    """
    Closes all the figures within pyplot.
    Consider doing this a disposable class together with get_plot.
    """
    pyplot.close()
