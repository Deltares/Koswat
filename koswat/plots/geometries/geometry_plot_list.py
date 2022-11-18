from typing import List

from matplotlib import pyplot
from shapely.geometry.base import BaseGeometry

from koswat.plots import get_cmap
from koswat.plots.geometries.geometry_plot import GeometryPlot
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class GeometryPlotList(KoswatPlotProtocol):
    koswat_object: List[BaseGeometry]
    subplot: pyplot.axes

    def plot(self, *args, **kwargs) -> pyplot.axes:
        _colors = get_cmap(n_colors=len(self.koswat_object))
        _geom_plot = GeometryPlot()
        _geom_plot.subplot = self.subplot
        for idx, _polygon in enumerate(self.koswat_object):
            _geom_plot.koswat_object = _polygon
            _geom_plot.plot(color=_colors(idx))
