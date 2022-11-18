from typing import List, Tuple

from matplotlib import pyplot

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.plots.dike.koswat_profile_plot import KoswatProfilePlot
from koswat.plots.koswat_plot_protocol import KoswatPlotProtocol


class ListKoswatProfilePlot(KoswatPlotProtocol):
    koswat_object: List[Tuple[KoswatProfileProtocol, str]]
    subplot: pyplot.axes

    def plot(self, *args, **kwargs) -> pyplot.axes:
        _profile_plot = KoswatProfilePlot()
        _profile_plot.subplot = self.subplot
        for _profile, _plot_color in self.koswat_object:
            _profile_plot.koswat_object = _profile
            _profile_plot.plot(unique_color=_plot_color)

        return self.subplot
