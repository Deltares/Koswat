import pytest
from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.cost_report.layer.layer_cost_report import LayerCostReport
from koswat.cost_report.layer.layer_cost_report_builder_protocol import (
    LayerCostReportBuilderProtocol,
)
from koswat.cost_report.layer.outside_slope_weakening_layer_cost_report_builder import (
    OustideSlopeWeakeningLayerCostReportBuilder,
)
from koswat.dike.layers.koswat_layers_wrapper import KoswatBaseLayer
from koswat.dike.material.koswat_material import KoswatMaterial


class TestOustideSlopeWeakiningLayerCostReportBuilder:
    def test_initialize(self):
        _builder = OustideSlopeWeakeningLayerCostReportBuilder()
        assert isinstance(_builder, OustideSlopeWeakeningLayerCostReportBuilder)
        assert isinstance(_builder, LayerCostReportBuilderProtocol)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.base_layer
        assert not _builder.calc_layer

    def test_given_different_material_when_build_then_raises(self):
        # 1. Define test data.
        _builder = OustideSlopeWeakeningLayerCostReportBuilder()
        _builder.base_layer = KoswatBaseLayer()
        _builder.base_layer.material = KoswatMaterial()
        _builder.base_layer.material.name = "a material"
        _builder.calc_layer = KoswatBaseLayer()
        _builder.calc_layer.material = KoswatMaterial()

        # 2. Run test
        with pytest.raises(ValueError) as exc_err:
            _builder.build()

        # 3. Verify expectations
        assert (
            str(exc_err.value)
            == "Material differs between layers. Cannot compute costs."
        )

    def test_given_same_material_when_build_then_returns_report(self):
        # 1. Define test data.
        _builder = OustideSlopeWeakeningLayerCostReportBuilder()
        _ref_point = Point(4.2, 2.4)
        _material_name = "Vibranium"
        _builder.base_layer = KoswatBaseLayer()
        _builder.base_layer.material = KoswatMaterial()
        _builder.base_layer.material.name = _material_name
        _builder.base_layer.geometry = _ref_point.buffer(2)
        _builder.calc_layer = KoswatBaseLayer()
        _builder.calc_layer.material = KoswatMaterial()
        _builder.calc_layer.material.name = _material_name
        _builder.calc_layer.geometry = _ref_point.buffer(4)

        # 2. Run test
        _layer_report = _builder.build()

        # 3. Verify expectations
        assert isinstance(_layer_report, LayerCostReport)
        assert _layer_report.new_layer == _builder.calc_layer
        assert _layer_report.old_layer == _builder.base_layer
        assert _layer_report.total_volume == pytest.approx(37.64, 0.001)
