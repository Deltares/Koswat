from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle


class TestSurroundingsObstacle:
    def test_initialize(self):
        # 1. Initialize
        _surrounding = SurroundingsObstacle()

        # 2. Verify expectations
        assert isinstance(_surrounding, SurroundingsObstacle)
        assert isinstance(_surrounding, KoswatSurroundingsProtocol)
        assert isinstance(_surrounding.points, list)
        assert len(_surrounding.points) == 0
