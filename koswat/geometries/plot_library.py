from typing import Any, List, Union

from matplotlib import pyplot
from shapely.geometry import MultiPolygon, Point, Polygon


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


def get_cmap(n_colors: int, name="hsv"):
    """
    Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.
    """
    return pyplot.cm.get_cmap(name, n_colors)


def plot_polygon(polygon: Union[Polygon, List[Point]], ax: pyplot.axes, color: str):
    """
    Plots a `Polygon` into the provided plot `ax` with the requested `color`.

    Args:
        polygon (Union[Polygon, List[Point], MultiPolygon]): Polygon to display.
        ax (pyplot.axes): Pyplot containing the drawing canvas.
        color (str): Color string.
    """
    dict_values = dict(color=color, linewidth=2, zorder=1)
    if isinstance(polygon, Polygon) and polygon.geom_type.lower() == "polygon":
        _x_coords, y_coords = polygon.boundary.coords.xy
        ax.plot(_x_coords, y_coords, **dict_values)
    elif isinstance(polygon, MultiPolygon):
        for geom in polygon.geoms:
            plot_polygon(geom, ax, color)
    elif isinstance(polygon, list):
        _x_points, _y_points = list(zip(*polygon))
        ax.scatter(_x_points, _y_points)


def plot_multiple_polygons(*args) -> pyplot:
    """
    Plots all provided polygons.

    Returns:
        pyplot: Canvas containig all drawings.
    """
    polygon_list = args
    fig = pyplot.figure(dpi=180)
    _subplot = fig.add_subplot()
    _colors = get_cmap(n_colors=len(polygon_list))
    for idx, _polygon in enumerate(polygon_list):
        plot_polygon(_polygon, _subplot, color=_colors(idx))

    return fig


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


def plot_highlight_layer(layer_list: List[Any], layer_to_highlight: Any) -> pyplot:
    """
    Plots a layer highlighting its content.

    Args:
        layer_list (List[Any]): List of layers to plot.
        layer_to_highlight (Any): Layer that requireds 'filling'.

    Returns:
        pyplot: Canvas containing all drawings.
    """
    fig = pyplot.figure(dpi=180)
    _subplot = fig.add_subplot()
    _colors = get_cmap(n_colors=len(layer_list))
    for idx, _layer in enumerate(layer_list):
        plot_layer(_layer, _subplot, color=_colors(idx))

    if isinstance(layer_to_highlight.geometry, Polygon):
        _x_coords, y_coords = layer_to_highlight.geometry.boundary.coords.xy
        _subplot.fill(_x_coords, y_coords)
    elif isinstance(layer_to_highlight.geometry, MultiPolygon):
        for _layer_geom in layer_to_highlight.geometry.geoms:
            _x_coords, y_coords = _layer_geom.boundary.coords.xy
            _subplot.fill(_x_coords, y_coords)
    return fig
