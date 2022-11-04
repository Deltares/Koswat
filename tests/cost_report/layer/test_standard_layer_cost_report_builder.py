import pytest

from koswat.cost_report.layer.layer_cost_report_builder_protocol import (
    LayerCostReportBuilderProtocol,
)
from koswat.cost_report.layer.standard_layer_cost_report_builder import (
    StandardLayerCostReportBuilder,
)
from koswat.dike.layers.koswat_base_layer import KoswatBaseLayer
from koswat.dike.material.koswat_material import KoswatMaterial


class TestStandardLayerCostReportBuilder:
    def test_initialize(self):
        _builder = StandardLayerCostReportBuilder()
        assert isinstance(_builder, StandardLayerCostReportBuilder)
        assert isinstance(_builder, LayerCostReportBuilderProtocol)
        assert not _builder.base_layer
        assert not _builder.calc_layer
        assert not _builder.base_core_geometry
        assert not _builder.wrapped_calc_geometry

    def test_build_different_material_raises(self):
        # 1. Define test data.
        _builder = StandardLayerCostReportBuilder()
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
