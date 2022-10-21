import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfile,
)
from koswat.calculations.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfile,
)
from koswat.cost_report.layer.layer_cost_report_builder_factory import (
    LayerCostReportBuilderFactory,
)
from koswat.cost_report.layer.layer_cost_report_builder_protocol import (
    LayerCostReportBuilderProtocol,
)
from koswat.cost_report.layer.outside_slope_weakening_layer_cost_report_builder import (
    OustideSlopeWeakeningLayerCostReportBuilder,
)
from koswat.cost_report.layer.standard_layer_cost_reinforcement_builder import (
    StandardLayerCostReportBuilder,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


class MockKoswatProfile(KoswatProfileProtocol):
    pass


class TestLayerCostReportBuilderFactory:
    def test_initialize(self):
        _factory = LayerCostReportBuilderFactory()
        assert isinstance(_factory, LayerCostReportBuilderFactory)

    def test_get_builder_unknown_type_raises(self):
        _expected_err = "No layer cost report builder available for {}".format(
            MockKoswatProfile
        )

        with pytest.raises(NotImplementedError) as exc_err:
            LayerCostReportBuilderFactory.get_builder(MockKoswatProfile)

        assert str(exc_err.value) == _expected_err

    @pytest.mark.parametrize(
        "reinforcement_type, expected_builder",
        [
            pytest.param(
                OutsideSlopeReinforcementProfile,
                OustideSlopeWeakeningLayerCostReportBuilder,
                id="OutsideSlopeReinforcement",
            ),
            pytest.param(
                StandardReinforcementProfile,
                StandardLayerCostReportBuilder,
                id="StandardReinforcement",
            ),
        ],
    )
    def test_get_builder_given_valid_type(
        self,
        reinforcement_type: KoswatProfileProtocol,
        expected_builder: LayerCostReportBuilderProtocol,
    ):
        _builder_type = LayerCostReportBuilderFactory.get_builder(reinforcement_type)
        _builder = _builder_type()
        assert isinstance(_builder, LayerCostReportBuilderProtocol)
        assert isinstance(_builder, expected_builder)
        assert isinstance(_builder, BuilderProtocol)
