from collections.abc import Callable, Iterator

import pytest
from shapely import Point

from koswat.dike.surroundings.point import PointInfrastructureSurroundings


@pytest.fixture(name="distances_to_surrounding_point_builder")
def get_distances_as_surrounding_point_builder() -> (
    Iterator[Callable[[Point, list[float]], PointInfrastructureSurroundings]]
):
    """
    Gets a builder to generate `PointInfrastructureSurroundings` with a location and a valid
    `surroundings_matrix` which could relate to an `ObstacleSurrounding`.

    Yields:
        Iterator[ Callable[[Point, list[float]], PointInfrastructureSurroundings] ]: Yields a builder of `PointInfrastructureSurroundings`.
    """

    def build_point_surroundings(
        location: Point, distances_list: list[float]
    ) -> PointInfrastructureSurroundings:
        return PointInfrastructureSurroundings(
            location=location, polderside_surroundings={_d: 1 for _d in distances_list}
        )

    yield build_point_surroundings
