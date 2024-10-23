from pathlib import Path

from koswat.cost_report.io.summary.summary_locations.cluster_collection_shp_fom import (
    ClusterCollectionShpFom,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class SummaryLocationsShpExporter:
    def export(self, koswat_summary: KoswatSummary, export_path: Path) -> None:
        if not export_path.exists():
            export_path.mkdir(parents=True)
        _measures = export_path.joinpath("summary_locations_measures.shp")
        _old = export_path.joinpath("summary_locations_old.shp")
        _new = export_path.joinpath("summary_locations_new.shp")

        # Get clusters
        _clusters = ClusterCollectionShpFom.from_summary(
            koswat_summary
        ).generate_geodataframes()

        if not _clusters:
            return

        _clusters[0].to_file(_measures)
        _clusters[1].to_file(_old)
        _clusters[2].to_file(_new)
