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
        _measures = export_path.joinpath("summary_locations_measures.shp")
        _old = export_path.joinpath("summary_locations_old.shp")
        _new = export_path.joinpath("summary_locations_new.shp")

        # Get clusters
        _lines_data = []
        _old_lines_data = []
        _new_lines_data = []
        for _profile_type, _locations in groupby(
            koswat_summary.reinforcement_per_locations,
            key=lambda x: x.selected_measure,
        ):
            _cluster = list(_locations)
            _report = koswat_summary.get_report_by_profile(_profile_type)
            _base_geometry = LineString([_l.location.location for _l in _cluster])
            _base_data = {
                "maatregel": _profile_type.__name__,
                "lengte": len(_cluster),
                "dijkbasis_oud": _report.profile_cost_report.reinforced_profile.old_profile.profile_width,
                "dijkbasis_nw": _report.profile_cost_report.reinforced_profile.profile_width,
            }
            _lines_data.append(_base_data | {"geometry": _base_geometry})
            _old_lines_data.append(
                _base_data
                | {
                    "geometry": _base_geometry.buffer(
                        -_base_data["dijkbasis_oud"], cap_style=2, single_sided=True
                    )
                }
            )
            _new_lines_data.append(
                _base_data
                | {
                    "geometry": _base_geometry.buffer(
                        -_base_data["dijkbasis_nw"], cap_style=2, single_sided=True
                    )
                }
            )
        _gdf = GeoDataFrame(_lines_data)
        _gdf.crs = "EPSG:28992"
        _gdf.to_file(_measures)

        ## BUFFERS
        _old_gdf = GeoDataFrame(_old_lines_data)
        _old_gdf.crs = "EPSG:28992"
        _old_gdf.to_file(_old)

        _new_gdf = GeoDataFrame(_new_lines_data)
        _new_gdf.crs = "EPSG:28992"
        _new_gdf.to_file(_new)
