from typing import List

from matplotlib import pyplot
from shapely.geometry import MultiPolygon, Polygon

from koswat.plots import get_cmap
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class HighlightGeometryPlot(KoswatPlotProtocol):
    koswat_object: Polygon

    def plot(self, subplot: pyplot.axes, *args, **kwargs) -> pyplot.axes:
        """
        Plots a layer highlighting its content.

        Args:
            subplot (pyplot.axes):  Pyplot containing the drawing canvas.
        """
        if isinstance(self.koswat_object, Polygon):
            _x_coords, y_coords = self.koswat_object.exterior.coords.xy
            subplot.fill(_x_coords, y_coords)
        elif isinstance(self.koswat_object, MultiPolygon):
            for _layer_geom in self.koswat_object.geoms:
                _x_coords, y_coords = _layer_geom.boundary.coords.xy
                subplot.fill(_x_coords, y_coords)
        return subplot
