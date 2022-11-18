from matplotlib import pyplot

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.plots.dike.koswat_layer_plot import KoswatLayerPlot
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class KoswatProfilePlot(KoswatPlotProtocol):
    koswat_object: KoswatProfileProtocol
    subplot: pyplot.axes

    def plot(self, color: str, *args, **kwargs) -> pyplot.axes:
        _layer_plot = KoswatLayerPlot()
        _layer_plot.subplot = self.subplot
        for _layer in self.koswat_object.layers_wrapper.layers:
            _layer_plot.koswat_object = _layer
            _layer_plot.plot(color)
        
        return self.subplot
