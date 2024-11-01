from copy import deepcopy
from typing import Iterator

import pytest

from koswat.cost_report.io.summary.summary_locations.cluster_collection_shp_fom import (
    ClusterCollectionShpFom,
)
from koswat.cost_report.io.summary.summary_locations.cluster_geodataframe_output_fom import (
    ClusterGeoDataFrameOutputFom,
)
from koswat.cost_report.io.summary.summary_locations.cluster_shp_fom import (
    ClusterShpFom,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class TestClustercollectionShpFom:
    def test_initialize(self):
        # 1. Define test data
        _fom = ClusterCollectionShpFom()

        # 2. Verify expectations
        assert isinstance(_fom, ClusterCollectionShpFom)
        assert not _fom.clusters
        assert _fom.crs_projection == "EPSG:28992"

    def test_from_summary(self, valid_mocked_summary: KoswatSummary):
        # 1. Run test.
        _fom = ClusterCollectionShpFom.from_summary(valid_mocked_summary)

        # 2. Verify expectations
        assert isinstance(_fom, ClusterCollectionShpFom)
        assert any(_fom.clusters)
        assert all(map(lambda x: isinstance(x, ClusterShpFom), _fom.clusters))

    @pytest.fixture(name="valid_fom")
    def _get_valid_cluster_collection_shp_fom(
        self, valid_mocked_summary: KoswatSummary
    ) -> Iterator[ClusterCollectionShpFom]:
        _fom = ClusterCollectionShpFom.from_summary(valid_mocked_summary)
        for _cluster in _fom.clusters:
            _locations = [_cl for _cl in _cluster.locations]
            for _l in _locations:
                _cluster.locations.append(deepcopy(_l))
        yield _fom

    def test_given_valid_fom_generate_geodataframes(
        self, valid_fom: ClusterCollectionShpFom
    ):
        # 1. Define test data.
        assert any(valid_fom.clusters)

        # 2. Run test.
        _gdf_output = valid_fom.generate_geodataframes()

        # 3. Verify expectations.
        assert isinstance(_gdf_output, ClusterGeoDataFrameOutputFom)
        assert _gdf_output.is_valid()
