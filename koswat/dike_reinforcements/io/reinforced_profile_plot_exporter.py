from pathlib import Path

from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementCoatingLayer,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.plots.dike.koswat_layers_wrapper_plot import KoswatLayersWrapperPlot
from koswat.plots.geometries.highlight_geometry_plot import HighlightGeometryPlot
from koswat.plots.koswat_figure_context_handler import KoswatFigureContextHandler
from koswat.plots.plot_exporter_protocol import PlotExporterProtocol


class ReinforcedProfilePlotExporter(PlotExporterProtocol):
    export_dir: Path
    reinforced_profile: ReinforcementProfileProtocol

    def export(self) -> None:
        _export_path = self.export_dir.joinpath(str(self.reinforced_profile))
        _export_path.mkdir(parents=True, exist_ok=True)
        self._displaying_layers(self.reinforced_profile, _export_path)

    def _displaying_layers(
        self, reinforced_profile: ReinforcementProfileProtocol, export_path: Path
    ):
        _layers_to_plot = []
        _layers_to_plot.extend(reinforced_profile.layers_wrapper.layers)
        _layers_to_plot.extend(reinforced_profile.old_profile.layers_wrapper.layers)

        for _reinf_layer in reinforced_profile.layers_wrapper.layers:
            _section_name = reinforced_profile.old_profile.input_data.dike_section
            _base_name = f"{reinforced_profile}_{_reinf_layer.material_type.name}"
            self._export_layers(
                export_path.joinpath(f"{_section_name}_added_{_base_name}"),
                _reinf_layer.new_layer_geometry,
                _layers_to_plot,
            )
            if isinstance(_reinf_layer, ReinforcementCoatingLayer):
                self._export_layers(
                    export_path.joinpath(f"{_section_name}_removed_{_base_name}"),
                    _reinf_layer.removal_layer_geometry,
                    _layers_to_plot,
                )

    def _export_layers(
        self,
        output_file: Path,
        layer_to_highlight,
        layers_to_plot: list[KoswatLayerProtocol],
    ):
        # Define canvas
        with KoswatFigureContextHandler(
            output_file.with_suffix(".png"), 180
        ) as _koswat_figure:
            _subplot = _koswat_figure.add_subplot()

            # Create plot builder for regular layers.
            _gpl_plot = KoswatLayersWrapperPlot.with_layers_list(layers_to_plot)
            _gpl_plot.subplot = _subplot
            _gpl_plot.plot()

            # Create plot builder for highlighted geom.
            _hg_plot = HighlightGeometryPlot()
            _hg_plot.koswat_object = layer_to_highlight
            _hg_plot.subplot = _subplot
            _hg_plot.plot()
