from koswat.dike.layers.layers_wrapper.koswat_layers_wrapper_builder_protocol import (
    KoswatLayersWrapperBuilderProtocol,
)
from koswat.dike_reinforcements.reinforcement_layers.outside_slope_reinforcement_layers_wrapper_builder import (
    OutsideSlopeReinforcementLayersWrapperBuilder,
)


class TestOutsideSlopeReinforcementLayersWrapperBuilder:
    def test_initialize(self):
        _builder = OutsideSlopeReinforcementLayersWrapperBuilder()
        assert isinstance(_builder, OutsideSlopeReinforcementLayersWrapperBuilder)
        assert isinstance(_builder, KoswatLayersWrapperBuilderProtocol)
