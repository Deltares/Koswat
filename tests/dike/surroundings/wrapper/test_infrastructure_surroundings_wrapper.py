from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.wrapper.base_surroundings_wrapper import (
    BaseSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)


class TestInfrastructureSurroundingsWrapper:
    def test_initialize(self):
        # 1. Define test data.
        _wrapper = InfrastructureSurroundingsWrapper()

        # 2. Verify expectations.
        assert isinstance(_wrapper, InfrastructureSurroundingsWrapper)
        assert isinstance(_wrapper, BaseSurroundingsWrapper)

        assert _wrapper.infrastructures_considered

        # Verify infras are initialized.
        assert isinstance(_wrapper.roads_class_2, SurroundingsInfrastructure)
        assert isinstance(_wrapper.roads_class_7, SurroundingsInfrastructure)
        assert isinstance(_wrapper.roads_class_24, SurroundingsInfrastructure)
        assert isinstance(_wrapper.roads_class_47, SurroundingsInfrastructure)
        assert isinstance(_wrapper.roads_class_unknown, SurroundingsInfrastructure)
