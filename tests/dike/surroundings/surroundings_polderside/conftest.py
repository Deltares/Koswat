from typing import Callable, Iterator

import pytest
from shapely import Point

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@pytest.fixture(name="surroundings_point_builder")
def get_surrounding_point_builder_fixture() -> Iterator[
    Callable[[Point, list[float]], PointSurroundings]
]:
    def create_point_surroundings(
        location: Point, distance_list: list[float]
    ) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = location
        _ps.distance_to_surroundings_dict = {_dl: 1 for _dl in distance_list}
        return _ps

    yield create_point_surroundings
