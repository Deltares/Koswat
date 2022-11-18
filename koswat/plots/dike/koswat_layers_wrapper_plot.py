from typing import Optional

from matplotlib import pyplot

from koswat.dike.layers.layers_wrapper import KoswatLayersWrapperProtocol
from koswat.plots import get_cmap
from koswat.plots.dike.koswat_layer_plot import KoswatLayerPlot
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class KoswatLayersWrapperPlot(KoswatPlotProtocol):
    koswat_object: KoswatLayersWrapperProtocol
    subplot: pyplot.axes

    def plot(self, unique_color: Optional[str], *args, **kwargs) -> pyplot.axes:
        _n_layers = len(self.koswat_object.layers)
        if unique_color:
            _colors = [unique_color] * _n_layers
        else:
            _colors = kwargs.get("color", get_cmap(n_colors=_n_layers))
        _layer_plot = KoswatLayerPlot()
        for idx, _polygon in enumerate(self.koswat_object.layers):
            _layer_plot.koswat_object = _polygon
            _layer_plot.plot(self.subplot, color=_colors(idx))
