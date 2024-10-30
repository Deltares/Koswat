from __future__ import annotations

from dataclasses import dataclass, field
from itertools import groupby
from typing import Type

from geopandas import GeoDataFrame

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
    def from_summary(cls, koswat_summary: KoswatSummary) -> ClusterCollectionShpFom:
        """
        Maps the `KoswatSummary` into a file object model that can be exported into `*.shp` files.

        Args:
            koswat_summary (KoswatSummary): The summary containing the information to export.

        Returns:
            ClusterCollectionShpFom: Dataclass instance that can be directly exported into `.shp`.
        """

        def to_cluster_shp_fom(
            key_group_tuple: tuple[
                Type[ReinforcementProfileProtocol], list[StrategyLocationReinforcement]
            ]
        ) -> ClusterShpFom:
            return ClusterShpFom(
                locations=list(key_group_tuple[1]),
                reinforced_profile=koswat_summary.get_report_by_profile(
                    key_group_tuple[0]
                ).profile_cost_report.reinforced_profile,
            )

        return cls(
            clusters=list(
                map(
                    to_cluster_shp_fom,
                    groupby(
                        koswat_summary.reinforcement_per_locations,
                        key=lambda x: x.current_selected_measure,
                    ),
                )
            )
        )

    def generate_geodataframes(self) -> tuple[GeoDataFrame, GeoDataFrame, GeoDataFrame]:
        """
        Generates all geodataframes of the given clusters. The generated geodataframes
        correspond to the, base geometry (without buffering), the old and new geometries
        with their profile's width being buffered to the base geometry.

        Returns:
            tuple[GeoDataFrame, GeoDataFrame, GeoDataFrame]:
                Tuple of geodataframes maping this `ClusterCollectionShpFom`.
        """

        def to_gdf_entry(
            cluster_shp_fom: ClusterShpFom,
        ) -> tuple[dict, dict, dict]:
            _base_dict = {
                "maatregel": cluster_shp_fom.reinforced_profile.output_name,
                "lengte": len(cluster_shp_fom.locations),
                "dijkbasis_oud": cluster_shp_fom.old_profile_width,
                "dijkbasis_nw": cluster_shp_fom.new_profile_width,
            }

            def buffered_entry(buffered_value: float) -> dict:
                return _base_dict | dict(
                    geometry=cluster_shp_fom.get_buffered_geometry(buffered_value)
                )

            return (
                _base_dict | dict(geometry=cluster_shp_fom.base_geometry),
                buffered_entry(cluster_shp_fom.old_profile_width),
                buffered_entry(cluster_shp_fom.new_profile_width),
            )

        def dict_list_to_gdf(dict_entries: list[dict]) -> GeoDataFrame:
            return GeoDataFrame(data=dict_entries, crs=self.crs_projection)

        return tuple(
            map(
                dict_list_to_gdf,
                zip(*(to_gdf_entry(_cl) for _cl in self.clusters)),
            )
        )
