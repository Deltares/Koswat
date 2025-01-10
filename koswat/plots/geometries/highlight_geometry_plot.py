from matplotlib import pyplot
from shapely.geometry import MultiPolygon, Polygon

from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class HighlightGeometryPlot(KoswatPlotProtocol):
    koswat_object: Polygon
    subplot: pyplot.axes

    def plot(self, *args, **kwargs) -> pyplot.axes:
        """
        Plots a layer highlighting its content.

        Returns:
            pyplot.axes: Polygon with its area painted.
        """
        _color = "#e377c2"
        if isinstance(self.koswat_object, Polygon):
            _x_coords, y_coords = self.koswat_object.exterior.coords.xy
            self.subplot.fill(_x_coords, y_coords)
        elif isinstance(self.koswat_object, MultiPolygon):
            for _layer_geom in self.koswat_object.geoms:
                _x_coords, y_coords = _layer_geom.boundary.coords.xy
                self.subplot.fill(_x_coords, y_coords)
        return self.subplot
