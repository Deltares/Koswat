import pytest

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class TestReinforcementProfileProtocol:
    def test_initialize_reinforcement_profile_raises(self):
        with pytest.raises(TypeError) as exc_err:
            ReinforcementProfileProtocol()

        assert str(exc_err.value) == "Protocols cannot be instantiated"
