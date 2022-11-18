from typing import List

from matplotlib import pyplot
from shapely.geometry.base import BaseGeometry

from koswat.plots import get_cmap
from koswat.plots.geometries.geometry_plot import GeometryPlot
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class GeometryPlotList(KoswatPlotProtocol):
    koswat_object: List[BaseGeometry]

    def plot(self, plot_axes: pyplot.axes):
        _colors = get_cmap(n_colors=len(self.koswat_object))
        _geom_plot = GeometryPlot()
        for idx, _polygon in enumerate(self.koswat_object):
            _geom_plot.koswat_geom = _polygon
            _geom_plot.plot(plot_axes, color=_colors(idx))
