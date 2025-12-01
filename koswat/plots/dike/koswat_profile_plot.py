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

from typing import Optional

from matplotlib import pyplot

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.plots.dike.koswat_layers_wrapper_plot import KoswatLayersWrapperPlot
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class KoswatProfilePlot(KoswatPlotProtocol):
    koswat_object: KoswatProfileProtocol
    subplot: pyplot.axes

    def plot(self, unique_color: Optional[str], *args, **kwargs) -> pyplot.axes:
        _layer_plot = KoswatLayersWrapperPlot()
        _layer_plot.subplot = self.subplot
        _layer_plot.koswat_object = self.koswat_object.layers_wrapper
        return _layer_plot.plot(unique_color=unique_color)
