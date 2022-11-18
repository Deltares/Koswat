from matplotlib import pyplot

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class KoswatLayerPlot(KoswatPlotProtocol):
    koswat_object: KoswatLayerProtocol
    subplot: pyplot.axes

    def plot(self, color: str) -> None:
        """
        Plots a `KoswatLayerProtocol` into the provided canvas `plot_axes` with the requested `color`.

        Args:
            color (str): Color code.

        Raises:
            ValueError: When the `KoswatLayerProtocol` material has not been registered.
        """
        _x_coords, y_coords = self.koswat_object.geometry.boundary.coords.xy
        dict_values = dict(color=color, linewidth=2, zorder=1)
        if self.koswat_object.material.name == "zand":
            dict_values["linestyle"] = "dashdot"
        elif self.koswat_object.material.name == "klei":
            dict_values["linestyle"] = "dashed"
        elif self.koswat_object.material.name == "gras":
            dict_values["linestyle"] = "solid"
        else:
            raise ValueError(
                f"Material {self.koswat_object.material.name} not supported for plotting."
            )
        self.subplot.plot(_x_coords, y_coords, **dict_values)
        _x_points, _y_points = list(zip(*self.koswat_object.upper_points.coords))
        self.subplot.scatter(_x_points, _y_points)
        return self.subplot
