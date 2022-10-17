import pytest
from shapely.geometry import Point

from koswat.cost_report.layer.layer_cost_report import LayerCostReport
from koswat.cost_report.profile.profile_cost_builder import ProfileCostReportBuilder
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.dike.layers.koswat_layers import KoswatBaseLayer, KoswatLayers
from koswat.dike.material.koswat_material import KoswatMaterial
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class TestProfileCostReportBuilder:
    def test_initialize(self):
        _builder = ProfileCostReportBuilder()
        assert isinstance(_builder, ProfileCostReportBuilder)
        assert not _builder.base_profile
        assert not _builder.calculated_profile

    def test_get_layer_cost_report_different_material_raises(self):
        # 1. Define test data.
        _builder = ProfileCostReportBuilder()
        _base_layer = KoswatBaseLayer()
        _base_layer.material = KoswatMaterial()
        _base_layer.material.name = "a material"
        _calc_layer = KoswatBaseLayer()
        _calc_layer.material = KoswatMaterial()

        # 2. Run test
        with pytest.raises(ValueError) as exc_err:
            _builder._get_layer_cost_report(_base_layer, _calc_layer)

        # 3. Verify expectations
        assert (
            str(exc_err.value)
            == "Material differs between layers. Cannot compute costs."
        )

    def _get_valid_profile_builder(self) -> ProfileCostReportBuilder:
        _builder = ProfileCostReportBuilder()
        _ref_point = Point(4.2, 2.4)
        _material_name = "Vibranium"
        _builder.base_profile = KoswatProfileBase()
        _base_layer = KoswatBaseLayer()
        _base_layer.material = KoswatMaterial()
        _base_layer.material.name = _material_name
        _base_layer.geometry = _ref_point.buffer(2)
        _builder.base_profile.layers_wrapper = KoswatLayers()
        _builder.base_profile.layers_wrapper.base_layer = _base_layer
        _builder.calculated_profile = KoswatProfileBase()
        _calc_layer = KoswatBaseLayer()
        _calc_layer.material = KoswatMaterial()
        _calc_layer.material.name = _material_name
        _calc_layer.geometry = _ref_point.buffer(4)
        _builder.calculated_profile.layers_wrapper = KoswatLayers()
        _builder.calculated_profile.layers_wrapper.base_layer = _calc_layer
        return _builder

    def test_get_layer_cost_report_same_material_returns_report(self):
        # 1. Define test data.
        _builder = ProfileCostReportBuilder()
        _ref_point = Point(4.2, 2.4)
        _material_name = "Vibranium"
        _base_layer = KoswatBaseLayer()
        _base_layer.material = KoswatMaterial()
        _base_layer.material.name = _material_name
        _base_layer.geometry = _ref_point.buffer(2)
        _calc_layer = KoswatBaseLayer()
        _calc_layer.material = KoswatMaterial()
        _calc_layer.material.name = _material_name
        _calc_layer.geometry = _ref_point.buffer(4)

        # 2. Run test
        _layer_report = _builder._get_layer_cost_report(_base_layer, _calc_layer)

        # 3. Verify expectations
        assert isinstance(_layer_report, LayerCostReport)
        assert _layer_report.new_layer == _calc_layer
        assert _layer_report.old_layer == _base_layer
        assert _layer_report.total_volume == pytest.approx(37.64, 0.001)

    def test_get_profile_cost_builder_different_layers_number_raises_error(self):
        # 1. Define test data.
        _builder = self._get_valid_profile_builder()
        _builder.calculated_profile.layers_wrapper = KoswatLayers()

        # 2. Run test
        with pytest.raises(ValueError) as exc_err:
            _builder._get_profile_cost_report()

        # 3. Verify expectations
        assert (
            str(exc_err.value)
            == "Layers not matching between old and new profile. Calculation of costs cannot be computed."
        )

    def test_get_profile_cost_report(self):
        # 1. Define test data.
        _builder = self._get_valid_profile_builder()

        # 2. Run test
        _profile_cost_report = _builder._get_profile_cost_report()

        # 3. Verify expectations
        self._validate_valid_profile_builder_build(_builder, _profile_cost_report)

    def test_build(self):
        # 1. Define test data.
        _builder = self._get_valid_profile_builder()

        # 2. Run test
        _profile_cost_report = _builder.build()

        # 3. Verify expectations
        self._validate_valid_profile_builder_build(_builder, _profile_cost_report)

    def _validate_valid_profile_builder_build(
        self, builder: ProfileCostReportBuilder, cost_report: ProfileCostReport
    ):
        assert isinstance(cost_report, ProfileCostReport)
        assert cost_report.new_profile == builder.calculated_profile
        assert len(cost_report.layer_cost_reports) == 1
        assert isinstance(cost_report.layer_cost_reports[0], LayerCostReport)
        assert cost_report.total_volume == pytest.approx(37.64, 0.001)
