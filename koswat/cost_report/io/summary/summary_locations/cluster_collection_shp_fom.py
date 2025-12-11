"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import groupby, pairwise
from typing import Callable, Type

from geopandas import GeoDataFrame

from koswat.cost_report.io.summary.summary_locations.cluster_geodataframe_output_fom import (
    ClusterGeoDataFrameOutputFom,
)
from koswat.cost_report.io.summary.summary_locations.cluster_shp_fom import (
    ClusterShpFom,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class ClusterCollectionShpFom:
    clusters: list[ClusterShpFom] = field(default_factory=lambda: [])
    crs_projection: str = "EPSG:28992"

    @classmethod
    def from_summary(
        cls,
        koswat_summary: KoswatSummary,
        cluster_criteria: Callable[
            [StrategyLocationReinforcement], type[ReinforcementProfileProtocol]
        ] = lambda x: x.current_selected_measure,
    ) -> ClusterCollectionShpFom:
        """
        Maps the `KoswatSummary` into a file object model that can be exported into `*.shp` files.

        Args:
            koswat_summary (KoswatSummary): The summary containing the information to export.
            cluster_criteria (Callable[
                [StrategyLocationReinforcement],
                type[ReinforcementProfileProtocol]
            ]): (Lambda) Function criteria to group the locations by reinforcement type.

        Returns:
            ClusterCollectionShpFom: Dataclass instance that can be directly exported into `.shp`.
        """

        def to_cluster_shp_fom(
            key_group_tuple: tuple[
                Type[ReinforcementProfileProtocol], list[StrategyLocationReinforcement]
            ],
        ) -> ClusterShpFom:
            return ClusterShpFom(
                locations=list(key_group_tuple[1]),
                reinforced_profile=koswat_summary.get_report_by_profile(
                    key_group_tuple[0]
                ).profile_cost_report.reinforced_profile,
            )

        _cluster_collection = cls(
            clusters=list(
                map(
                    to_cluster_shp_fom,
                    groupby(
                        koswat_summary.reinforcement_per_locations,
                        key=cluster_criteria,
                    ),
                )
            )
        )

        # Add neighbour extent to clusters
        for _cluster in pairwise(_cluster_collection.clusters):
            ClusterShpFom.add_neighbour_extent(_cluster[0], _cluster[1])

        return _cluster_collection

    def generate_geodataframes(self) -> ClusterGeoDataFrameOutputFom:
        """
        Generates all geodataframes of the given clusters. The generated geodataframes
        correspond to the, base geometry (without buffering), the old and new geometries
        with their profile's width being buffered to the base geometry.

        Returns:
            ClusterGeoDataFrameOutputFom: Resulting geodataframes wrapper maping this `ClusterCollectionShpFom`.
        """

        def to_gdf_entry(
            cluster_shp_fom: ClusterShpFom,
        ) -> tuple[dict, dict, dict]:
            _base_dict = {
                "dijkvak": cluster_shp_fom.reinforced_profile.input_data.dike_section,
                "maatregel": cluster_shp_fom.reinforced_profile.output_name,
                "lengte": len(cluster_shp_fom.locations),
                "bs_pld_oud": cluster_shp_fom.old_polderside_width,
                "bs_pld_nw": cluster_shp_fom.new_polderside_width,
            }

            def buffered_entry(buffered_value: float) -> dict:
                return _base_dict | dict(
                    geometry=cluster_shp_fom.get_buffered_geometry(buffered_value)
                )

            return (
                _base_dict | dict(geometry=cluster_shp_fom.base_geometry),
                buffered_entry(cluster_shp_fom.old_polderside_width),
                buffered_entry(cluster_shp_fom.new_polderside_width),
            )

        def dict_list_to_gdf(dict_entries: list[dict]) -> GeoDataFrame:
            return GeoDataFrame(data=dict_entries, crs=self.crs_projection)

        return ClusterGeoDataFrameOutputFom(
            tuple(
                map(
                    dict_list_to_gdf,
                    zip(*(to_gdf_entry(_cl) for _cl in self.clusters)),
                )
            )
        )
