from typing import List

from matplotlib import pyplot
from shapely.geometry import MultiPolygon, Polygon


def plot_layer(layer, ax: pyplot.axes, color: str):
    """
    Plots a Koswat layer into the provided canvas `ax` with the requested `color`.

    Args:
        layer (KoswatLayerProtocol): Koswat layer containing a geometry.
        ax (pyplot.axes): Canvas.
        color (str): Color code.

    Raises:
        ValueError: When the `layer` material has not been registered.
    """
    _x_coords, y_coords = layer.geometry.boundary.coords.xy
    dict_values = dict(color=color, linewidth=2, zorder=1)
    if layer.material.name == "zand":
        dict_values["linestyle"] = "dashdot"
    elif layer.material.name == "klei":
        dict_values["linestyle"] = "dashed"
    elif layer.material.name == "gras":
        dict_values["linestyle"] = "solid"
    else:
        raise ValueError(f"Material {layer.material.name} not supported for plotting.")
    ax.plot(_x_coords, y_coords, **dict_values)
    _x_points, _y_points = list(zip(*layer.upper_points.coords))
    ax.scatter(_x_points, _y_points)


def plot_multiple_layers(*args) -> pyplot:
    """
    Plots all provided Koswat Layers.

    Returns:
        pyplot: Canvas containing all drawings.
    """
    _layer_list = args
    fig = pyplot.figure(dpi=180)
    _subplot = fig.add_subplot()
    _colors = get_cmap(n_colors=len(_layer_list))
    for idx, _layer in enumerate(_layer_list):
        plot_layer(_layer, _subplot, color=_colors(idx))

    return fig


def plot_highlight_geometry(
    geometry_list: List[Polygon], layer_to_highlight: Polygon
) -> pyplot:
    """
    Plots a layer highlighting its content.

    Args:
        layer_list (List[Polygon]): List of layers to plot.
        layer_to_highlight (Polygon): Layer that requireds 'filling'.

    Returns:
        pyplot: Canvas containing all drawings.
    """
    fig = pyplot.figure(dpi=180)
    _subplot = fig.add_subplot()
    _colors = get_cmap(n_colors=len(geometry_list))
    for idx, _layer in enumerate(geometry_list):
        plot_layer(_layer, _subplot, color=_colors(idx))

    if isinstance(layer_to_highlight, Polygon):
        _x_coords, y_coords = layer_to_highlight.exterior.coords.xy
        _subplot.fill(_x_coords, y_coords)
    elif isinstance(layer_to_highlight, MultiPolygon):
        for _layer_geom in layer_to_highlight.geoms:
            _x_coords, y_coords = _layer_geom.boundary.coords.xy
            _subplot.fill(_x_coords, y_coords)
    return fig
