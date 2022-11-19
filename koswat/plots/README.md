# Koswat.Plots

This module is intended to contain all logic regarding plotting (but not so much as to export). This way we can reduced the dependencies and leave the rest of the modules independent from this logic.

The module is divided in sub-modules. Each one trying to represent the upper domain modules to delegate responsibilites. For instance, plottings related to `koswawt.dike` will be found at `koswat.plots.dike` module.

At the root of this module we define the generic protocols and classes.
- `utils.py`: Contains all relevant methods that could be used across the entire module. Eventually could be moved to __init__.py.
- `KoswatPlotProtocol`: `Protocol` to represent a `Koswat` object that needs to be plotted.
- `KoswatFigureContextHandler`: Context handler that initializes a `matplotlib.figure` instance and exports its plots to a defined `pathlib.Path` during `__exit__`.
- `PlotExporterProtocol`: Contract needed to be fulfilled when defining concrete exporters related to plots.