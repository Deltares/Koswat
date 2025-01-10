from pathlib import Path

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.summary_locations.cluster_collection_shp_fom import (
    ClusterCollectionShpFom,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class SummaryLocationsShpExporter(KoswatExporterProtocol):
    def export(self, koswat_summary: KoswatSummary, export_path: Path) -> None:
        if not export_path.exists():
            export_path.mkdir(parents=True)
        _measures = export_path.joinpath("summary_locations_measures.shp")
        _old = export_path.joinpath("summary_locations_old.shp")
        _new = export_path.joinpath("summary_locations_new.shp")

        # Get clusters comparing old to new.
        _clusters = ClusterCollectionShpFom.from_summary(
            koswat_summary, lambda x: x.current_selected_measure
        ).generate_geodataframes()

        if not _clusters.is_valid():
            return

        # Export clusters to file
        _clusters.base_layer.to_file(_measures)
        _clusters.initial_state.to_file(_old)
        _clusters.new_state.to_file(_new)

        # Get clusters for steps
        _step_clusters = ClusterCollectionShpFom.from_summary(
            koswat_summary, lambda x: x.get_selected_measure_steps()[1]
        ).generate_geodataframes()

        if not _step_clusters.is_valid():
            return

        # Export clusters to file
        _step_clusters.new_state.to_file(
            export_path.joinpath("summary_locations_step.shp")
        )
