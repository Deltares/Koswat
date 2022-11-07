import pytest
from shapely.geometry import Point, Polygon

from koswat.calculations import StandardReinforcementProfile
from koswat.calculations.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.cost_report.layer.base_layer_cost_report import BaseLayerCostReport
from koswat.cost_report.layer.standard_layer_cost_report import StandardLayerCostReport
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.cost_report.profile.standard_profile_cost_report_builder import (
    StandardProfileCostReportBuilder,
)
from koswat.dike.layers.koswat_layers_wrapper import (
    KoswatBaseLayer,
    KoswatLayersWrapper,
)
from koswat.dike.material.koswat_material import KoswatMaterial
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class TestStandardProfileCostReportBuilder:
    def test_initialize(self):
        _builder = StandardProfileCostReportBuilder()
        assert isinstance(_builder, StandardProfileCostReportBuilder)
        assert isinstance(_builder, ProfileCostReportBuilderProtocol)
        assert not _builder.base_profile
        assert not _builder.calculated_profile

    def _get_valid_profile_builder(self) -> StandardProfileCostReportBuilder:
        _builder = StandardProfileCostReportBuilder()
        _ref_point = Point(4.2, 2.4)
        _material_name = "Vibranium"
        _builder.base_profile = KoswatProfileBase()
        _base_layer = KoswatBaseLayer()
        _base_layer.material = KoswatMaterial()
        _base_layer.material.name = _material_name
        _base_layer.geometry = _ref_point.buffer(2)
        _builder.base_profile.layers_wrapper = KoswatLayersWrapper()
        _builder.base_profile.layers_wrapper.base_layer = _base_layer
        _builder.calculated_profile = CofferdamReinforcementProfile()
        _calc_layer = KoswatBaseLayer()
        _calc_layer.material = KoswatMaterial()
        _calc_layer.material.name = _material_name
        _calc_layer.geometry = _ref_point.buffer(4)
        _builder.calculated_profile.layers_wrapper = KoswatLayersWrapper()
        _builder.calculated_profile.layers_wrapper.base_layer = _calc_layer
        return _builder

    def test_given_different_layers_number_when_build_then_raises_error(self):
        # 1. Define test data.
        _builder = self._get_valid_profile_builder()
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
        _builder = self._get_valid_profile_builder()

        # 2. Run test
        _profile_cost_report = _builder.build()

        # 3. Verify expectations
        self._validate_valid_profile_builder_build(_builder, _profile_cost_report)

    def _validate_valid_profile_builder_build(
        self,
        builder: StandardProfileCostReportBuilder,
        cost_report: ProfileCostReport,
    ):
        assert isinstance(cost_report, ProfileCostReport)
        assert cost_report.new_profile == builder.calculated_profile
        assert len(cost_report.layer_cost_reports) == 1
        # The core layer report is a basic one (sand)
        assert isinstance(cost_report.layer_cost_reports[0], BaseLayerCostReport)
        assert cost_report.total_volume == pytest.approx(37.64, 0.001)
