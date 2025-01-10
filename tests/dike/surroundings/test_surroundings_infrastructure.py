from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)


class TestSurroundingsInfrastructure:
    def test_initialize(self):
        # 1. Initialize
        _surrounding = SurroundingsInfrastructure()

        # 2. Verify expectations
        assert isinstance(_surrounding, SurroundingsInfrastructure)
        assert isinstance(_surrounding, KoswatSurroundingsProtocol)
        assert isinstance(_surrounding.points, list)
        assert len(_surrounding.points) == 0
