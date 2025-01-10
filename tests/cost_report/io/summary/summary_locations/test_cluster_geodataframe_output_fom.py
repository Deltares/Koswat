from geopandas import GeoDataFrame

from koswat.cost_report.io.summary.summary_locations.cluster_geodataframe_output_fom import (
    ClusterGeoDataFrameOutputFom,
)


class TestClusterGeodataframeOutputFom:
    def test_initialize_with_none_tuple(self):
        # 1. Run test.
        _fom = ClusterGeoDataFrameOutputFom(None)

        # 2. Verify expectations.
        assert _fom.is_valid() is False
        assert _fom.base_layer is None
        assert _fom.initial_state is None
        assert _fom.new_state is None

    def test_initialize_with_valid_tuple(self):
        # 1. Define test data
        _base_value = GeoDataFrame()
        _initial_value = GeoDataFrame()
        _new_value = GeoDataFrame()

        # 2. Run test.
        _fom = ClusterGeoDataFrameOutputFom(
            tuple((_base_value, _initial_value, _new_value))
        )

        # 3. Verify expectations.
        assert _fom.is_valid()
        assert _fom.base_layer.equals(_base_value)
        assert _fom.initial_state.equals(_initial_value)
        assert _fom.new_state.equals(_new_value)
