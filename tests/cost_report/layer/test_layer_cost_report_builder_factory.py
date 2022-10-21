import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfileProtocol,
)
from koswat.calculations.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfileProtocol,
)
from koswat.cost_report.layer.layer_cost_report_builder_factory import (
    LayerCostReportBuilderFactory,
)
from koswat.cost_report.layer.layer_cost_report_builder_protocol import (
    LayerCostReportBuilderProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


class MockStandardReinforcement(StandardReinforcementProfileProtocol):
    pass


class MockOutsideSlopeReinforcement(OutsideSlopeReinforcementProfileProtocol):
    pass


class MockKoswatProfile(KoswatProfileProtocol):
    pass


class TestLayerCostReportBuilderFactory:
    def test_initialize(self):
        _factory = LayerCostReportBuilderFactory()
        assert isinstance(_factory, LayerCostReportBuilderFactory)

    def test_get_builder_unknown_type_raises(self):
        _koswat_profile = MockKoswatProfile()
        _expected_err = "No layer cost report builder available for {}".format(
            _koswat_profile
        )

        with pytest.raises(NotImplementedError) as exc_err:
            LayerCostReportBuilderFactory.get_builder(_koswat_profile)

        assert str(exc_err.value) == _expected_err

    @pytest.mark.parametrize(
        "reinforcement_type",
        [
            pytest.param(MockOutsideSlopeReinforcement, id="OutsideSlopeReinforcement"),
            pytest.param(MockStandardReinforcement, id="StandardReinforcement"),
        ],
    )
    def test_get_builder_given_valid_type(
        self, reinforcement_type: KoswatProfileProtocol
    ):
        _builder_type = LayerCostReportBuilderFactory.get_builder(reinforcement_type())
        _builder = _builder_type()
        assert isinstance(_builder, LayerCostReportBuilderProtocol)
        assert isinstance(_builder, BuilderProtocol)
