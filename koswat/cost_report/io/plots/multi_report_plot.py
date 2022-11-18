from pathlib import Path

from koswat.calculations.reinforcement_layers_wrapper import ReinforcementCoatingLayer
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.plots import get_plot
from koswat.plots.dike.koswat_profile_plot import KoswatProfilePlot
from koswat.plots.dike.list_koswat_profile_plot import ListKoswatProfilePlot
from koswat.plots.geometries import HighlightGeometryPlot
from koswat.plots.geometries.geometry_plot_list import GeometryPlotList


class MultiLocationProfilePlot:
    report: MultiLocationProfileCostReport
    export_dir: Path

    def _comparing_profiles(self, file_path: Path):
        # Define canvas
        _figure = get_plot(180)
        _subplot = _figure.add_subplot()

        # Create plot builder.
        _list_profile_plot = ListKoswatProfilePlot()
        _list_profile_plot.koswat_object = [
            (self.report.profile_cost_report.reinforced_profile.old_profile, "#03a9fc"),
            (self.report.profile_cost_report.reinforced_profile, "#fc0303"),
        ]
        _list_profile_plot.subplot = _subplot
        _list_profile_plot.plot()

        # Export plots
        _figure.savefig(file_path)

    def _export_layers(self, output_file: Path, geom_to_highlight, geoms_to_plot):
        # Define cavnas
        _figure = get_plot(180)
        _subplot = _figure.add_subplot()

        # Create plot builder for regular layers.
        _gpl_plot = GeometryPlotList()
        _gpl_plot.koswat_object = geoms_to_plot
        _gpl_plot.subplot = _subplot
        _gpl_plot.plot()

        # Create plot builder for highlighted geom.
        _hg_plot = HighlightGeometryPlot()
        _hg_plot.koswat_object = geom_to_highlight
        _hg_plot.subplot = _subplot
        _hg_plot.plot()

        # Export figure.
        _figure.savefig(output_file.with_suffix(".png"))

    def _displaying_layers(self, reinforced_profile: ReinforcementProfileProtocol):
        _layers_to_plot = []
        _layers_to_plot.extend(reinforced_profile.layers_wrapper.layers)
        _layers_to_plot.extend(reinforced_profile.old_profile.layers_wrapper.layers)
        _export_dir: Path = self.export_dir / str(reinforced_profile)
        _export_dir.mkdir(parents=True, exist_ok=True)

        for _reinf_layer in reinforced_profile.layers_wrapper.layers:
            _base_name = f"{reinforced_profile}_{_reinf_layer.material.name}"
            self._export_layers(
                _export_dir / f"added_{_base_name}",
                _reinf_layer.new_layer_geometry,
                _layers_to_plot,
            )
            if isinstance(_reinf_layer, ReinforcementCoatingLayer):
                self._export_layers(
                    _export_dir / f"removed_{_base_name}",
                    _reinf_layer.removal_layer_geometry,
                    _layers_to_plot,
                )

    def export(self):
        _fig_filepath = self.export_dir / self.report.profile_type
        self._comparing_profiles(_fig_filepath.with_suffix(".png"))
        self._displaying_layers(self.report.profile_cost_report.reinforced_profile)
