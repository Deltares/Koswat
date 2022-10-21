from matplotlib import pyplot
from shapely import affinity

from koswat.calculations import ReinforcementProfileProtocol
from koswat.cost_report.layer.layer_cost_report import LayerCostReport
from koswat.cost_report.layer.standard_layer_cost_reinforcement_builder import (
    StandardLayerCostReportBuilder,
)
from koswat.cost_report.layer.standard_layer_cost_report import StandardLayerCostReport
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_base_layer import KoswatBaseLayer
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


def plot_layer(layer: KoswatLayerProtocol, ax: pyplot.axes, color: str):
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


class StandardProfileCostReportBuilder(ProfileCostReportBuilderProtocol):
    base_profile: KoswatProfileProtocol
    calculated_profile: ReinforcementProfileProtocol

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.calculated_profile = None

    def _get_layer_cost_report(
        self,
        base_layer: KoswatLayerProtocol,
        calculated_layer: KoswatLayerProtocol,
        core_layer: KoswatLayerProtocol,
    ) -> StandardLayerCostReport:
        _report = StandardLayerCostReport()
        _report.old_layer = base_layer
        _report.core_layer = core_layer
        _report.removed_layer = KoswatBaseLayer()
        _report.removed_layer.geometry = calculated_layer.geometry.difference(
            core_layer.geometry
        )
        _report.removed_layer.material = calculated_layer.material
        _report.new_layer = KoswatBaseLayer()
        _report.new_layer.geometry = calculated_layer.geometry.difference(
            core_layer.geometry
        )
        _report.new_layer.material = calculated_layer.material
        _report.new_layer = calculated_layer
        pl1 = plot_layers(_report.core_layer, _report.removed_layer)
        pl2 = plot_layers(_report.core_layer, _report.new_layer)
        return _report

    def _get_base_layer_report(
        self, old_base_layer: KoswatBaseLayer, new_base_layer: KoswatBaseLayer
    ) -> StandardLayerCostReport:
        _report = StandardLayerCostReport()
        _report.old_layer = old_base_layer
        _report.removed_layer = None
        _diff_geometry = new_base_layer.geometry.difference(old_base_layer.geometry)
        _report.new_layer = KoswatBaseLayer()
        _report.new_layer.geometry = _diff_geometry
        _report.new_layer.material = new_base_layer.material
        # _report.new_layer.upper_points = _diff_geometry.coords
        # pl = plot_layers(_report.old_layer, _report.new_layer)
        return _report

    def _get_new_core_layer(
        self, core_layer: KoswatLayerProtocol, depth: float
    ) -> KoswatLayerProtocol:
        _moved_geom = affinity.translate(core_layer.geometry, xoff=-depth, yoff=0.0)
        _new_layer = KoswatBaseLayer()
        _new_layer.geometry = _moved_geom.union(core_layer.geometry)
        _new_layer.material = core_layer.material
        # pl = plot_layers(core_layer, _new_layer)
        return _new_layer

    def build(self) -> ProfileCostReport:
        _report = ProfileCostReport()
        _report.new_profile = self.calculated_profile
        _report.old_profile = self.base_profile
        if len(self.base_profile.layers_wrapper.layers) != len(
            self.calculated_profile.layers_wrapper.layers
        ):
            raise ValueError(
                "Layers not matching between old and new profile. Calculation of costs cannot be computed."
            )

        _core_layer_report = self._get_base_layer_report(
            self.base_profile.layers_wrapper.base_layer,
            self.calculated_profile.layers_wrapper.base_layer,
        )
        pl = plot_layers(_core_layer_report.old_layer, _core_layer_report.new_layer)
        _core_layer = _core_layer_report.old_layer
        for idx_l, old_l in reversed(
            list(enumerate(self.base_profile.layers_wrapper.coating_layers))
        ):
            _calculated_layer = self.calculated_profile.layers_wrapper.coating_layers[
                idx_l
            ]
            _core_layer = self._get_new_core_layer(_core_layer, _calculated_layer.depth)
            _layer_report = self._get_layer_cost_report(
                old_l, _calculated_layer, _core_layer
            )

            _report.layer_cost_reports.append(_layer_report)

        _report.layer_cost_reports.append(_core_layer_report)
        return _report
