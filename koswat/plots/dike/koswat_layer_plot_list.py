from typing import List

from matplotlib import pyplot

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.plots import get_cmap
from koswat.plots.dike.koswat_layer_plot import KoswatLayerPlot
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class KoswatLayerPlotList(KoswatPlotProtocol):
    koswat_object: List[KoswatLayerProtocol]

    def plot(self, plot_axes: pyplot.axes):
        # _subplot = fig.add_subplot()
        _colors = get_cmap(n_colors=len(self.koswat_object))
        _layer_plot = KoswatLayerPlot()
        for idx, _polygon in enumerate(self.koswat_object):
            _layer_plot.koswat_object = _polygon
            _layer_plot.plot(plot_axes, color=_colors(idx))
