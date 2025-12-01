"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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

from __future__ import annotations

from matplotlib import pyplot

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike.layers.layers_wrapper import KoswatLayersWrapperProtocol
from koswat.plots import get_cmap
from koswat.plots.dike.koswat_layer_plot import KoswatLayerPlot
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class KoswatLayersWrapperPlot(KoswatPlotProtocol):
    koswat_object: KoswatLayersWrapperProtocol
    subplot: pyplot.axes

    def plot(self, *args, **kwargs) -> pyplot.axes:
        _n_layers = len(self.koswat_object.layers)
        _unique_color = kwargs.get("unique_color", None)
        _colors = get_cmap(n_colors=_n_layers)
        _layer_plot = KoswatLayerPlot()
        _layer_plot.subplot = self.subplot
        for idx, _polygon in enumerate(self.koswat_object.layers):
            _layer_plot.koswat_object = _polygon
            _layer_plot.plot(color=_unique_color if _unique_color else _colors(idx))

    @classmethod
    def with_layers_list(
        cls, layers_list: list[KoswatLayerProtocol]
    ) -> KoswatLayersWrapperPlot:
        """
        Class method to aid the usage of this class with unrelated layers from different wrappers.

        Args:
            layers_list (list[KoswatLayerProtocol]): List of layers to wrap just for plotting.

        Returns:
            KoswatLayersWrapperPlot: Initialized valid instance with custom intenal wrapper `PlotLayersWrapper`.
        """

        class PlotLayersWrapper(KoswatLayersWrapperProtocol):
            layers: list[KoswatLayerProtocol]

        _plot = cls()
        _wrapper = PlotLayersWrapper()
        _wrapper.layers = layers_list
        _plot.koswat_object = _wrapper
        return _plot
