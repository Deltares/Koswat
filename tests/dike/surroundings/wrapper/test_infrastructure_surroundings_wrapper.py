from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)


class TestInfrastructureSurroundingsWrapper:
    def test_initialize(self):
        # 1. Define test data.
        _wrapper = InfrastructureSurroundingsWrapper()

        # 2. Verify expectations.
        assert isinstance(_wrapper, InfrastructureSurroundingsWrapper)

        assert _wrapper.infrastructures_considered

        # Verify infras are initialized.
        assert not _wrapper.infrastructures_collection
