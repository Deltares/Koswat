"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from matplotlib import pyplot
from numpy import concatenate
from shapely.geometry import LineString, MultiLineString

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layer_protocol import (
    ReinforcementLayerProtocol,
)
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class KoswatLayerPlot(KoswatPlotProtocol):
    koswat_object: KoswatLayerProtocol
    subplot: pyplot.axes

    @staticmethod
    def _get_xy_line_coords(
        koswat_geometry: LineString | MultiLineString,
    ) -> tuple[list[float], list[float]]:
        if isinstance(koswat_geometry, LineString):
            return tuple(map(list, koswat_geometry.coords.xy))

        return tuple(
            map(concatenate, zip(*map(lambda x: x.coords.xy, koswat_geometry.geoms)))
        )

    def plot(self, color: str) -> None:
        """
        Plots a `KoswatLayerProtocol` into the provided canvas `plot_axes` with the requested `color`.

        Args:
            color (str): Color code.

        return list(
            map(concatenate, zip(*map(lambda x: x.coords.xy, koswat_geometry.geoms)))
        )
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

        if isinstance(self.koswat_object, ReinforcementLayerProtocol):
            _surface_x, _surface_y = self._get_xy_line_coords(
                self.koswat_object.new_layer_surface
            )
            self.subplot.plot(
                _surface_x,
                _surface_y,
                color="#000",
                linewidth=2,
                zorder=1,
                linestyle="solid",
            )
        return self.subplot
