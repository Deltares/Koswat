from pathlib import Path

from matplotlib import pyplot
from pytest import FixtureRequest

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol

test_data = Path(__file__).parent / "test_data"
test_results = Path(__file__).parent / "test_results"

if not test_results.is_dir():
    test_results.mkdir(parents=True)


def get_fixturerequest_case_name(request: FixtureRequest):
    _case_name_idx = request.node.name.index("[") + 1
    _case_name = (
        request.node.name[_case_name_idx:-1].lower().replace(" ", "_").replace("-", "_")
    )
    return _case_name


def plot_layer(layer: KoswatLayerProtocol, ax: pyplot.axes, color: str):
    _x_coords, y_coords = zip(*layer.upper_points.coords)
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


def plot_profile(
    subplot: pyplot.axes, profile: KoswatProfileProtocol, color: str
) -> None:
    for _layer in profile.layers_wrapper.layers:
        plot_layer(_layer, subplot, color)


def plot_profiles(
    base_profile: KoswatProfileProtocol, reinforced_profile: KoswatProfileProtocol
) -> pyplot:
    fig = pyplot.figure(1, dpi=90)
    _subplot = fig.add_subplot(221)
    plot_profile(_subplot, base_profile, color="#03a9fc")
    plot_profile(_subplot, reinforced_profile, color="#fc0303")
    return fig
