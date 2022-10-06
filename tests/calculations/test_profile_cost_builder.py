import math

import pytest
from shapely.geometry import Point

from koswat.cost_report.builders.profile_cost_builder import ProfileCostBuilder
from koswat.cost_report.reports.layer_cost_report import LayerCostReport
from koswat.cost_report.reports.profile_cost_report import ProfileCostReport
from koswat.profiles.koswat_layers import KoswatBaseLayer, KoswatLayers
from koswat.profiles.koswat_material import KoswatMaterial
from koswat.profiles.koswat_profile import KoswatProfileBase


class TestProfileCostBuilder:
    def test_initialize(self):
        _builder = ProfileCostBuilder()
        assert isinstance(_builder, ProfileCostBuilder)
        assert not _builder.base_profile
        assert not _builder.calculated_profile

    def test_get_layer_cost_report_different_material_raises(self):
        # 1. Define test data.
        _builder = ProfileCostBuilder()
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

    def test_get_layer_cost_report_same_material_returns_report(self):
        # 1. Define test data.
        _builder = ProfileCostBuilder()
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

        assert _layer_report.total_volume == pytest.approx(37.64, 0.001)

    def test_get_profile_cost_report(self):
        # 1. Define test data.
        _builder = ProfileCostBuilder()
        _ref_point = Point(4.2, 2.4)
        _material_name = "Vibranium"
        _builder.base_profile = KoswatProfileBase()
        _base_layer = KoswatBaseLayer()
        _base_layer.material = KoswatMaterial()
        _base_layer.material.name = _material_name
        _base_layer.geometry = _ref_point.buffer(2)
        _builder.base_profile.layers = KoswatLayers()
        _builder.base_profile.layers.base_layer = _base_layer
        _builder.calculated_profile = KoswatProfileBase()
        _calc_layer = KoswatBaseLayer()
        _calc_layer.material = KoswatMaterial()
        _calc_layer.material.name = _material_name
        _calc_layer.geometry = _ref_point.buffer(4)
        _builder.calculated_profile.layers = KoswatLayers()
        _builder.calculated_profile.layers.base_layer = _calc_layer

        # 2. Run test
        _profile_cost_report = _builder._get_profile_cost_report()

        # 3. Verify expectations
        assert isinstance(_profile_cost_report, ProfileCostReport)
        assert _profile_cost_report.new_profile == _builder.calculated_profile
        assert len(_profile_cost_report.layer_cost_reports) == 1
        assert isinstance(_profile_cost_report.layer_cost_reports[0], LayerCostReport)
        assert _profile_cost_report.layer_cost_reports[0].new_layer == _calc_layer
        assert _profile_cost_report.total_volume == pytest.approx(37.64, 0.001)

    def test_get_profile_cost_builder_different_layers_number_raises_error(self):
        # 1. Define test data.
        _builder = ProfileCostBuilder()
        _ref_point = Point(4.2, 2.4)
        _material_name = "Vibranium"
        _builder.base_profile = KoswatProfileBase()
        _base_layer = KoswatBaseLayer()
        _base_layer.material = KoswatMaterial()
        _base_layer.material.name = _material_name
        _base_layer.geometry = _ref_point.buffer(2)
        _builder.base_profile.layers = KoswatLayers()
        _builder.base_profile.layers.base_layer = _base_layer
        _builder.calculated_profile = KoswatProfileBase()
        _calc_layer = KoswatBaseLayer()
        _calc_layer.material = KoswatMaterial()
        _calc_layer.material.name = _material_name
        _calc_layer.geometry = _ref_point.buffer(4)
        _builder.calculated_profile.layers = KoswatLayers()

        # 2. Run test
        with pytest.raises(ValueError) as exc_err:
            _builder._get_profile_cost_report()

        # 3. Verify expectations
        assert (
            str(exc_err.value)
            == "Layers not matching between old and new profile. Calculation of costs cannot be computed."
        )

    def test_build(
        self,
    ):
        # 1. Define test data.
        _builder = ProfileCostBuilder()
        _ref_point = Point(4.2, 2.4)
        _material_name = "Vibranium"
        _builder.base_profile = KoswatProfileBase()
        _base_layer = KoswatBaseLayer()
        _base_layer.material = KoswatMaterial()
        _base_layer.material.name = _material_name
        _base_layer.geometry = _ref_point.buffer(2)
        _builder.base_profile.layers = KoswatLayers()
        _builder.base_profile.layers.base_layer = _base_layer
        _builder.calculated_profile = KoswatProfileBase()
        _calc_layer = KoswatBaseLayer()
        _calc_layer.material = KoswatMaterial()
        _calc_layer.material.name = _material_name
        _calc_layer.geometry = _ref_point.buffer(4)
        _builder.calculated_profile.layers = KoswatLayers()
        _builder.calculated_profile.layers.base_layer = _calc_layer

        # 2. Run test
        _profile_cost_report = _builder.build()

        # 3. Verify expectations
        assert isinstance(_profile_cost_report, ProfileCostReport)
        assert _profile_cost_report.new_profile == _builder.calculated_profile
        assert len(_profile_cost_report.layer_cost_reports) == 1
        assert isinstance(_profile_cost_report.layer_cost_reports[0], LayerCostReport)
        assert _profile_cost_report.layer_cost_reports[0].new_layer == _calc_layer
        assert _profile_cost_report.total_volume == pytest.approx(37.64, 0.001)
