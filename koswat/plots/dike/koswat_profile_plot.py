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
