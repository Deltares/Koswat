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
