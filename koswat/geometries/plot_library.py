from matplotlib import pyplot


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


def plot_layers(layer_left, layer_right) -> pyplot:
    fig = pyplot.figure(dpi=180)
    _subplot = fig.add_subplot()
    plot_layer(layer_left, _subplot, color="#03a9fc")
    plot_layer(layer_right, _subplot, color="#fc0303")
    return fig


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
