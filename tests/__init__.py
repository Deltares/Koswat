import shutil
from pathlib import Path

from matplotlib import pyplot
from pytest import FixtureRequest

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.geometries import plot_layer, plot_layers

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


def get_testcase_results_dir(request: FixtureRequest) -> Path:
    _case_name = get_fixturerequest_case_name(request)
    _test_dir: Path = test_results / request.node.originalname
    _test_dir.mkdir(exist_ok=True, parents=True)
    _test_dir = _test_dir / _case_name
    if _test_dir.is_dir():
        shutil.rmtree(_test_dir)
    _test_dir.mkdir(parents=True)
    return _test_dir


def plot_profile(
    subplot: pyplot.axes, profile: KoswatProfileProtocol, color: str
) -> None:
    for _layer in profile.layers_wrapper.layers:
        plot_layer(_layer, subplot, color)


def plot_profiles(
    base_profile: KoswatProfileProtocol, reinforced_profile: KoswatProfileProtocol
) -> pyplot:
    fig = pyplot.figure(dpi=180)
    _subplot = fig.add_subplot()
    plot_profile(_subplot, base_profile, color="#03a9fc")
    plot_profile(_subplot, reinforced_profile, color="#fc0303")

    return fig
