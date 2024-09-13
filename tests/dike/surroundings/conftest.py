from typing import Callable, Iterator

import pytest
from shapely import Point

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@pytest.fixture(name="distances_to_surrounding_point_builder")
def get_distances_as_surrounding_point_builder() -> Iterator[
    Callable[[Point, list[float]], PointSurroundings]
]:
    def build_point_surroundings(
        location: Point, distances_list: list[float]
    ) -> PointSurroundings:
        return PointSurroundings(
            location=location, surroundings_matrix={_d: 1 for _d in distances_list}
        )

    yield build_point_surroundings
