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
