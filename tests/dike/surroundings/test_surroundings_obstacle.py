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

    def test_when_get_locations_after_distance(self):
        # 1. Define test data.
        _surrounding = SurroundingsObstacle()

        # 2. Run test.
        _classified_surroundings = _surrounding.get_locations_after_distance()

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, dict)
        assert not _classified_surroundings

    def test_when_get_classify_surroundings_given_points_then_dict_with_locations(self):
        pass
