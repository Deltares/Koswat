from typing import Callable, Iterable

import pytest
from shapely import Point

from koswat.dike.surroundings.point.point_obstacle_surroundings import PointObstacleSurroundings
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)


@pytest.fixture(name="buildings_obstacle_surroundings_fixture")
def _get_buildings_fixture() -> Iterable[
    Callable[[list[tuple[Point, float]]], ObstacleSurroundingsWrapper]
]:
    def build_surroundings_wrapper(
        point_distances: list[tuple[Point, float]]
    ) -> ObstacleSurroundingsWrapper:
        _points = [
            PointObstacleSurroundings(
                location=_pd[0],
                inside_distance=_pd[1],
            )
            for _pd in point_distances
        ]
        _obstacle = SurroundingsObstacle(points=_points)
        return ObstacleSurroundingsWrapper(
            buildings=_obstacle,
        )

    yield build_surroundings_wrapper
