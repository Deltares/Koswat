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
