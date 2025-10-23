from typing import Callable, Iterable

import pytest
from shapely import Point

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)


@pytest.fixture(name="buildings_obstacle_surroundings_fixture")
def _get_buildings_fixture() -> Iterable[
    Callable[[list[tuple[Point, list[float]]]], ObstacleSurroundingsWrapper]
]:
    def build_surroundings_wrapper(
        point_distances: list[tuple[Point, list[float]]]
    ) -> ObstacleSurroundingsWrapper:
        _points = [
            PointSurroundings(
                location=_pd[0], surroundings_matrix={_d: 1 for _d in _pd[1]}
            )
            for _pd in point_distances
        ]
        _obstacle = SurroundingsObstacle(points=_points)
        return ObstacleSurroundingsWrapper(
            apply_buildings=True,
            buildings=_obstacle,
        )

    yield build_surroundings_wrapper
