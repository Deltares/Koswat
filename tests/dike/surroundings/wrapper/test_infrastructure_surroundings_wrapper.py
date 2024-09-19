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

        # Verify supported infras are initialized.
        assert isinstance(_wrapper.roads_class_2_polderside, SurroundingsInfrastructure)
        assert isinstance(_wrapper.roads_class_7_polderside, SurroundingsInfrastructure)
        assert isinstance(
            _wrapper.roads_class_24_polderside, SurroundingsInfrastructure
        )
        assert isinstance(
            _wrapper.roads_class_47_polderside, SurroundingsInfrastructure
        )
        assert isinstance(
            _wrapper.roads_class_unknown_polderside, SurroundingsInfrastructure
        )

        # Verify unsupported infras are not initialized.
        assert not _wrapper.roads_class_2_dikeside
        assert not _wrapper.roads_class_7_dikeside
        assert not _wrapper.roads_class_24_dikeside
        assert not _wrapper.roads_class_47_dikeside
        assert not _wrapper.roads_class_unknown_dikeside
