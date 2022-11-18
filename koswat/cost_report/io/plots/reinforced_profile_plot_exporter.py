from pathlib import Path
from typing import List

from koswat.calculations.reinforcement_layers_wrapper import ReinforcementCoatingLayer
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.plots import close_figure, get_plot
from koswat.plots.dike.koswat_layers_wrapper_plot import KoswatLayersWrapperPlot
from koswat.plots.geometries.highlight_geometry_plot import HighlightGeometryPlot
from koswat.plots.plot_exporter_protocol import PlotExporterProtocol


class ReinforcedProfilePlotExporter(PlotExporterProtocol):
    export_dir: Path

    def export(self, plot_object_model: ReinforcementProfileProtocol) -> None:
        # _fig_filepath = self.export_filepath / self._cost_report.profile_type
        _export_path: Path = self.export_dir / str(plot_object_model)
        _export_path.mkdir(parents=True, exist_ok=True)
        self._displaying_layers(plot_object_model, _export_path)

    def _displaying_layers(self, reinforced_profile: ReinforcementProfileProtocol, export_path: Path):
        _layers_to_plot = []
        _layers_to_plot.extend(reinforced_profile.layers_wrapper.layers)
        _layers_to_plot.extend(reinforced_profile.old_profile.layers_wrapper.layers)

        for _reinf_layer in reinforced_profile.layers_wrapper.layers:
            _base_name = f"{reinforced_profile}_{_reinf_layer.material.name}"
            self._export_layers(
                export_path / f"added_{_base_name}",
                _reinf_layer.new_layer_geometry,
                _layers_to_plot,
            )
            if isinstance(_reinf_layer, ReinforcementCoatingLayer):
                self._export_layers(
                    export_path / f"removed_{_base_name}",
                    _reinf_layer.removal_layer_geometry,
                    _layers_to_plot,
                )

    def _export_layers(
        self,
        output_file: Path,
        layer_to_highlight,
        layers_to_plot: List[KoswatLayerProtocol],
    ):
        # Define cavnas
        _figure = get_plot(180)
        _subplot = _figure.add_subplot()

        # Create plot builder for regular layers.
        _gpl_plot = KoswatLayersWrapperPlot.with_layers_list(layers_to_plot)
        _gpl_plot.subplot = _subplot
        _gpl_plot.plot()

        # Create plot builder for highlighted geom.
        _hg_plot = HighlightGeometryPlot()
        _hg_plot.koswat_object = layer_to_highlight
        _hg_plot.subplot = _subplot
        _hg_plot.plot()

        # Export figure.
        _figure.savefig(output_file.with_suffix(".png"))
        close_figure()
