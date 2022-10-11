from pathlib import Path

from matplotlib import pyplot
from pytest import FixtureRequest
from shapely import geometry

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol

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


def plot_line(ax, ob, color):
    parts = hasattr(ob, "geoms") and ob or [ob]
    for part in parts:
        x, y = part.xy
        ax.plot(x, y, color=color, linewidth=3, solid_capstyle="round", zorder=1)


def plot_profiles(
    base_profile: KoswatProfileProtocol, reinforced_profile: KoswatProfileProtocol
) -> pyplot:
    fig = pyplot.figure(1, dpi=90)
    _subplot = fig.add_subplot(221)
    plot_line(_subplot, geometry.LineString(base_profile.points), color="#03a9fc")
    plot_line(_subplot, geometry.LineString(reinforced_profile.points), color="#fc0303")
    return fig
