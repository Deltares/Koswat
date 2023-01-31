import pytest

from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.profile.volume_cost_parameters_builder import (
    VolumeCostParametersBuilder,
)


class TestVolumeCostParametersBuilder:
    def test_initialize(self):
        _builder = VolumeCostParametersBuilder()
        assert isinstance(_builder, VolumeCostParametersBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert _builder.reinforced_profile is None
        assert _builder.koswat_costs is None

    def test_no_reinforced_profile_raises(self):
        _expected_mssg = "No reinforced profile provided."
        with pytest.raises(ValueError) as exc_value:
            _builder = VolumeCostParametersBuilder()
            _builder.koswat_costs = None
            _builder.reinforced_profile = None
            _builder.build()

        assert str(exc_value.value) == _expected_mssg

    def test_no_koswat_costs_raises(self):
        _expected_mssg = "No koswat costs provided."
        with pytest.raises(ValueError) as exc_value:
            _builder = VolumeCostParametersBuilder()
            _builder.koswat_costs = None
            _builder.reinforced_profile = None
            _builder.build()

        assert str(exc_value.value) == _expected_mssg
