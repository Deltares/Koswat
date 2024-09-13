from typing import Callable, Iterator

import pytest
from shapely import Point

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@pytest.fixture(name="distances_to_surrounding_point_builder")
def get_distances_as_surrounding_point_builder() -> Iterator[
    Callable[[Point, list[float]], PointSurroundings]
]:
    """
    Gets a builder to generate `PointSurroundings` with a location and a valid
    `surroundings_matrix` which could relate to an `ObstacleSurrounding`.

    Yields:
        Iterator[ Callable[[Point, list[float]], PointSurroundings] ]: Yields a builder of `PointSurroundings`.
    """

    def build_point_surroundings(
        location: Point, distances_list: list[float]
    ) -> PointSurroundings:
        return PointSurroundings(
            location=location, surroundings_matrix={_d: 1 for _d in distances_list}
        )

    yield build_point_surroundings
