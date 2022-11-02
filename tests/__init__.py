import shutil
from pathlib import Path

from matplotlib import pyplot
from pytest import FixtureRequest

from koswat.cost_report.layer.standard_layer_cost_report import StandardLayerCostReport
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.geometries.plot_library import (
    plot_highlight_layer,
    plot_layer,
    plot_multiple_layers,
)

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


def export_multi_report_plots(multi_report, export_dir: Path):
    def _comparing_profiles():
        _profiles_plots = plot_profiles(
            multi_report.profile_cost_report.old_profile,
            multi_report.profile_cost_report.new_profile,
        )
        _fig_file = export_dir / multi_report.profile_type
        _fig_file.with_suffix(".png")
        _profiles_plots.savefig(_fig_file)

    _comparing_profiles()

    def _comparing_layers(report: ProfileCostReport, report_name: str):
        for _layer_c_report in report.layer_cost_reports:
            _layers_to_plot = []
            _layers_to_plot.append(report.new_profile.layers_wrapper.coating_layers[0])
            _layers_to_plot.append(_layer_c_report.new_layer)
            _layers_to_plot.append(_layer_c_report.old_layer)
            _material = _layer_c_report.material
            _legend = [
                "New Dike Profile",
                f"New {_material} layer",
                f"Old {_material} layer",
            ]
            if isinstance(_layer_c_report, StandardLayerCostReport):
                _layers_to_plot.append(_layer_c_report.core_layer)
                if _layer_c_report.removed_layer:
                    _layers_to_plot.append(_layer_c_report.removed_layer)
                _legend.extend(["Core layer", f"Removed {_material} layer"])

            _fig_file = export_dir / f"{report_name}_{_material}"
            _fig_file.with_suffix(".png")
            _layers_plots = plot_multiple_layers(_layers_to_plot)
            _layers_plots.legend(_legend)
            _layers_plots.savefig(_fig_file)

    def _displaying_layers(report: ProfileCostReport, report_name: str):
        def _export_layers(layer_type: str, layer, layers_to_plot):
            _fig_file = export_dir / layer_type
            _fig_file.with_suffix(".png")
            _layers_plots = plot_highlight_layer(layers_to_plot, layer)
            _layers_plots.savefig(_fig_file)

        _layers_to_plot = []
        _layers_to_plot.extend(report.old_profile.layers_wrapper.layers)
        _layers_to_plot.extend(report.new_profile.layers_wrapper.layers)
        for _layer_c_report in report.layer_cost_reports:
            if isinstance(_layer_c_report, StandardLayerCostReport):
                _export_layers(
                    f"{report_name}_new_{_layer_c_report.material}",
                    _layer_c_report.new_layer,
                    _layers_to_plot,
                )
                if _layer_c_report.removed_layer:
                    _export_layers(
                        f"{report_name}_removal_{_layer_c_report.material}",
                        _layer_c_report.removed_layer,
                        _layers_to_plot,
                    )

    _comparing_layers(multi_report.profile_cost_report, multi_report.profile_type)
    _displaying_layers(multi_report.profile_cost_report, multi_report.profile_type)
