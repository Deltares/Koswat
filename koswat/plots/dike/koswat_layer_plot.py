from matplotlib import pyplot

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol
from shapely import geometry
from numpy import concatenate


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
        _x_coords, y_coords = self.koswat_object.outer_geometry.boundary.coords.xy
        dict_values = dict(color=color, linewidth=2, zorder=1)
        if self.koswat_object.material_type == KoswatMaterialType.SAND:
            dict_values["linestyle"] = "dashdot"
        elif self.koswat_object.material_type == KoswatMaterialType.CLAY:
            dict_values["linestyle"] = "dashed"
        elif self.koswat_object.material_type == KoswatMaterialType.GRASS:
            dict_values["linestyle"] = "solid"
        else:
            raise ValueError(
                f"Material {self.koswat_object.material_type.name} not supported for plotting."
            )
        self.subplot.plot(_x_coords, y_coords, **dict_values)
        _x_points, _y_points = list(zip(*self.koswat_object.upper_points.coords))
        self.subplot.scatter(_x_points, _y_points)
        from koswat.calculations.reinforcement_layers_wrapper import (
            ReinforcementLayerProtocol,
        )

        if isinstance(self.koswat_object, ReinforcementLayerProtocol):
            if isinstance(self.koswat_object.new_layer_surface, geometry.Polygon):
                _surface_x, _surface_y = self.koswat_object.new_layer_surface.coords.xy
                self.subplot.plot(
                    _surface_x,
                    _surface_y,
                    color="#000",
                    linewidth=2,
                    zorder=1,
                    linestyle="solid",
                )
            if isinstance(self.koswat_object.new_layer_surface, geometry.MultiPolygon):
                _combined_xy = list(
                    map(
                        concatenate(
                            zip(
                                self.koswat_object.new_layer_surface.geoms[0].coords.xy,
                                self.koswat_object.new_layer_surface.geoms[1].coords.xy,
                            )
                        )
                    )
                )
                self.subplot.plot(
                    _combined_xy[0],
                    _combined_xy[1],
                    color="#000",
                    linewidth=2,
                    zorder=1,
                    linestyle="solid",
                )
        return self.subplot
