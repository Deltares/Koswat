from typing import Callable, Type

from geopandas import GeoDataFrame
from shapely import LineString

from koswat.cost_report.io.summary.summary_locations.cluster_collection_shp_fom import (
    ClusterCollectionShpFom,
    ClusterGeoDataFrameOutputFom,
)
from koswat.cost_report.io.summary.summary_locations.cluster_shp_fom import (
    ClusterShpFom,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.vps_reinforcement_profile import (
    VPSReinforcementProfile,
)


class TestClusterCollectionShpFom:
    _default_crs_projection = "EPSG:28992"

    def test_initialize(self):
        _fom = ClusterCollectionShpFom()

        assert isinstance(_fom, ClusterCollectionShpFom)
        assert _fom.crs_projection == self._default_crs_projection
        assert not any(_fom.clusters)

    def test_from_summary_initializes_clusters(
        self, valid_clusters_mocked_summary: KoswatSummary
    ):
        # 1. Define and run test data.
        _fom = ClusterCollectionShpFom.from_summary(valid_clusters_mocked_summary)

        # 2. Verify expectations.
        assert isinstance(_fom, ClusterCollectionShpFom)
        assert _fom.crs_projection == self._default_crs_projection
        assert len(_fom.clusters) == 1
        assert all(
            isinstance(_fom_cluster, ClusterShpFom) for _fom_cluster in _fom.clusters
        )

    def test_given_clusters_when_generate_geodataframes_then_gets_expected_gdf(
        self,
        cluster_shp_fom_factory: Callable[
            [list[tuple[float, float]], Type[ReinforcementProfileProtocol], float],
            ClusterShpFom,
        ],
    ):
        # 1. Define test data.
        _clusters_reference_data = [
            cluster_shp_fom_factory([(0, 0), (0, 2)], SoilReinforcementProfile, 4.2),
            cluster_shp_fom_factory(
                [(1, 2), (2, 2), (3, 2)], VPSReinforcementProfile, 2.4
            ),
            cluster_shp_fom_factory([(3, 2), (4, 2)], SoilReinforcementProfile, 4.2),
        ]
        _cluster_collection = ClusterCollectionShpFom(clusters=_clusters_reference_data)
        assert isinstance(_cluster_collection, ClusterCollectionShpFom)

        # 2. Run test.
        _gdf_collection = _cluster_collection.generate_geodataframes()

        # 3. Verify xpectations.
        assert isinstance(_gdf_collection, ClusterGeoDataFrameOutputFom)

        def check_gdf(
            gdf_result: GeoDataFrame,
            geometry_lambda: Callable[[ClusterShpFom], LineString],
        ):
            assert isinstance(gdf_result, GeoDataFrame)
            assert gdf_result.crs == self._default_crs_projection
            assert list(gdf_result.columns) == [
                "maatregel",
                "lengte",
                "dijkbasis_oud",
                "dijkbasis_nw",
                "geometry",
            ]
            assert len(gdf_result.values) == len(_clusters_reference_data)
            # They should be in order, so the following should be correct
            for _idx, _cluster_value in enumerate(gdf_result.values):
                _ref_data = _clusters_reference_data[_idx]
                assert _cluster_value[0] == _ref_data.reinforced_profile.output_name
                assert _cluster_value[1] == len(_ref_data.locations)
                assert _cluster_value[2] == _ref_data.old_profile_width
                assert _cluster_value[3] == _ref_data.new_profile_width
                assert _cluster_value[4] == geometry_lambda(_ref_data)

        check_gdf(
            _gdf_collection.base_layer,
            lambda c_fom: c_fom.base_geometry,
        )
        check_gdf(
            _gdf_collection.initial_state,
            lambda c_fom: c_fom.get_buffered_geometry(c_fom.old_profile_width),
        )
        check_gdf(
            _gdf_collection.new_state,
            lambda c_fom: c_fom.get_buffered_geometry(c_fom.new_profile_width),
        )
