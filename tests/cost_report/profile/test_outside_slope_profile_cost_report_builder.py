import pytest
from shapely.geometry import Point

from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfile,
)
from koswat.cost_report.layer.coating_layer_cost_report import CoatingLayerCostReport
from koswat.cost_report.profile.outside_slope_profile_cost_report_builder import (
    OutsideSlopeProfileCostReportBuilder,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.dike.layers.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layers_wrapper import (
    KoswatBaseLayer,
    KoswatLayersWrapper,
)
from koswat.dike.material.koswat_material import KoswatMaterial
from tests.cost_report import get_valid_profile_builder


class TestOutsideSlopeProfileCostReportBuilder:
    def test_initialize(self):
        _builder = OutsideSlopeProfileCostReportBuilder()
        assert isinstance(_builder, OutsideSlopeProfileCostReportBuilder)
        assert not _builder.base_profile
        assert not _builder.calculated_profile

    def test_get_layer_cost_report_different_material_raises(self):
        class MockReinforcement(OutsideSlopeReinforcementProfile):
            pass

        # 1. Define test data.
        _builder = OutsideSlopeProfileCostReportBuilder()
        _builder.calculated_profile = MockReinforcement()
        _base_layer = KoswatBaseLayer()
        _base_layer.material = KoswatMaterial()
        _base_layer.material.name = "a material"
        _calc_layer = KoswatBaseLayer()
        _calc_layer.material = KoswatMaterial()

        # 2. Run test
        with pytest.raises(ValueError) as exc_err:
            _builder._get_layer_cost_report(_base_layer, _calc_layer, None, None)

        # 3. Verify expectations
        assert (
            str(exc_err.value)
            == "Material differs between layers. Cannot compute costs."
        )

    def test_get_layer_cost_report_oustide_slope_reinforcement_profile_same_material_returns_report(
        self,
    ):
        class MockReinforcement(OutsideSlopeReinforcementProfile):
            pass

        # 1. Define test data.
        _builder = OutsideSlopeProfileCostReportBuilder()
        _builder.calculated_profile = MockReinforcement()
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
        _layer_report = _builder._get_layer_cost_report(
            _base_layer, _calc_layer, _ref_point.buffer(1), _ref_point.buffer(3)
        )

        # 3. Verify expectations
        assert isinstance(_layer_report, CoatingLayerCostReport)
        assert _layer_report.new_layer == _calc_layer
        assert _layer_report.old_layer == _base_layer
        assert isinstance(_layer_report.added_layer, KoswatCoatingLayer)
        assert _layer_report.added_layer.geometry
        assert _layer_report.added_layer.layer_points
        assert _layer_report.added_layer.upper_points
        assert _layer_report.total_volume == pytest.approx(21.95, 0.001)

    def test_given_different_layers_number_when_build_then_raises_error(self):
        # 1. Define test data.
        _builder = get_valid_profile_builder(OutsideSlopeProfileCostReportBuilder)
        _builder.calculated_profile.layers_wrapper = KoswatLayersWrapper()

        # 2. Run test
        with pytest.raises(ValueError) as exc_err:
            _builder.build()

        # 3. Verify expectations
        assert (
            str(exc_err.value)
            == "Layers not matching between old and new profile. Calculation of costs cannot be computed."
        )

    def test_build(self):
        # 1. Define test data.
        _builder = get_valid_profile_builder(OutsideSlopeProfileCostReportBuilder)

        # 2. Run test
        _profile_cost_report = _builder.build()

        # 3. Verify expectations
        self._validate_valid_profile_builder_build(_builder, _profile_cost_report)

    def _validate_valid_profile_builder_build(
        self,
        builder: OutsideSlopeProfileCostReportBuilder,
        cost_report: ProfileCostReport,
    ):
        assert isinstance(cost_report, ProfileCostReport)
        assert cost_report.new_profile == builder.calculated_profile
        assert len(cost_report.layer_cost_reports) == 1
        assert all(
            isinstance(lcr, CoatingLayerCostReport)
            for lcr in cost_report.layer_cost_reports
        )
        assert cost_report.total_volume == pytest.approx(37.64, 0.001)
