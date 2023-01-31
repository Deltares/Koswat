from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_layers_wrapper_builder import (
    OutsideSlopeReinforcementLayersWrapperBuilder,
)
from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper_builder_protocol import (
    KoswatLayersWrapperBuilderProtocol,
)


class TestOutsideSlopeReinforcementLayersWrapperBuilder:
    def test_initialize(self):
        _builder = OutsideSlopeReinforcementLayersWrapperBuilder()
        assert isinstance(_builder, OutsideSlopeReinforcementLayersWrapperBuilder)
        assert isinstance(_builder, KoswatLayersWrapperBuilderProtocol)
