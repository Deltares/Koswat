# -*- coding: utf-8 -*-
from itertools import groupby
from pathlib import Path

from geopandas import GeoDataFrame
from shapely.geometry import LineString

from koswat.cost_report.summary.koswat_summary import KoswatSummary


class SummaryLocationsShpExporter:
    def export(self, koswat_summary: KoswatSummary, export_path: Path) -> None:
        if not export_path.exists():
            export_path.mkdir(parents=True)
        _base_path = export_path.joinpath("summary_locations.shp")
        _measures = _base_path.with_name(_base_path.name + "_measures")
        _old = _base_path.with_name(_base_path.name + "_old")
        _new = _base_path.with_name(_base_path.name + "_new")

        # Get clusters
        _lines_data = []
        for _profile_type, _locations in groupby(
            koswat_summary.reinforcement_per_locations,
            key=lambda x: x.selected_measure,
        ):
            _cluster = list(_locations)
            _lines_data.append(
                {
                    "geometry": LineString([_l.location.location for _l in _cluster]),
                    "maatregel": _profile_type.__name__,
                    "lengte": len(_cluster),
                    "dijkbasis_oud": 23,
                    "dijkbasis_nw": 42,
                }
            )
        _gdf = GeoDataFrame(_lines_data)
        _gdf.crs = "EPSG:28992"
        _gdf.to_file(_measures)

        # Get linestring per cluster

        # Determine start and end of each section.

        # Get width per cluster - per point
        # lines_data.append(
        #     {
        #         "coordinates": coords,
        #         "maatregel": maatregel,
        #         "lengte": len(coords),
        #         "dijkbasis_oud": dijkbasis_oud,
        #         "dijkbasis_nw": dijkbasis_nw,
        #     }
        # )
        # pass
