from typing import List, Union

from matplotlib import pyplot
from shapely.geometry import GeometryCollection, MultiPolygon, Point, Polygon

from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class GeometryPlot(KoswatPlotProtocol):
    koswat_object: Union[Polygon, List[Point]]

    def _plot_simple_polygon(self, plot_axes: pyplot.axes, color: str):
        _dict_values = dict(color=color, linewidth=2, zorder=1)
        _x_coords, y_coords = self.koswat_object.boundary.coords.xy
        plot_axes.plot(_x_coords, y_coords, **_dict_values)

    def _plot_simple_polygon_list(self, plot_axes: pyplot.axes):
        _x_points, _y_points = list(zip(*self.koswat_object))
        plot_axes.scatter(_x_points, _y_points)

    def _plot_multi_polygon(self, plot_axes: GeometryCollection, color: str):
        for geom in self.koswat_object.geoms:
            self.plot(geom, plot_axes, color)

    def plot(self, plot_axes: pyplot.axes, color: str):
        """
        Plots a `Polygon` into the provided plot `ax` with the requested `color`.

        Args:
            polygon (Union[Polygon, List[Point], MultiPolygon]): Polygon to display.
            ax (pyplot.axes): Pyplot containing the drawing canvas.
            color (str): Color string.
        """
        if (
            isinstance(self.koswat_object, Polygon)
            and self.koswat_object.geom_type.lower() == "polygon"
        ):
            self._plot_simple_polygon(plot_axes, color)
        elif isinstance(self.koswat_object, MultiPolygon):
            self._plot_multi_polygon(self.koswat_object.geoms, color)
        elif isinstance(self.koswat_object, list):
            self._plot_simple_polygon_list(plot_axes)
