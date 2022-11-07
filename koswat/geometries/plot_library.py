from typing import Any, List, Union

from matplotlib import pyplot
from shapely.geometry import MultiPolygon, Point, Polygon


def plot_layer(layer, ax: pyplot.axes, color: str):
    # _x_coords, y_coords = zip(*layer.upper_points.coords)
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
    # _x_coords, y_coords = zip(*layer.upper_points.coords)
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
    polygon_list = args
    fig = pyplot.figure(dpi=180)
    _subplot = fig.add_subplot()
    _colors = get_cmap(n_colors=len(polygon_list))
    for idx, _polygon in enumerate(polygon_list):
        plot_polygon(_polygon, _subplot, color=_colors(idx))

    return fig


def plot_multiple_layers(layer_list: List[Any]) -> pyplot:
    fig = pyplot.figure(dpi=180)
    _subplot = fig.add_subplot()
    _colors = get_cmap(n_colors=len(layer_list))
    for idx, _layer in enumerate(layer_list):
        plot_layer(_layer, _subplot, color=_colors(idx))

    return fig


def plot_highlight_layer(layer_list: List[Any], layer_to_highlight: Any) -> pyplot:
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


def plot_layers(layer_left, layer_right) -> pyplot:
    return plot_multiple_layers([layer_left, layer_right])


def plot_polygons(pol_left, pol_right) -> pyplot:
    fig = pyplot.figure(dpi=180)
    _subplot = fig.add_subplot()

    def plot_polygon(pol, ax: pyplot.axes, color):
        dict_values = dict(linestyle="dashdot", color=color, linewidth=2, zorder=1)
        x, y = pol.boundary.xy
        ax.plot(x, y, **dict_values)

    plot_polygon(pol_left, _subplot, color="#03a9fc")
    plot_polygon(pol_right, _subplot, color="#fc0303")
    return fig
