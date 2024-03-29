from __future__ import annotations

from typing import List, Tuple

from shapely.geometry import Point


class CharacteristicPoints:
    p_1: Point
    p_2: Point
    p_3: Point
    p_4: Point
    p_5: Point
    p_6: Point
    p_7: Point
    p_8: Point

    def __init__(self) -> None:
        self.p_1 = None
        self.p_2 = None
        self.p_3 = None
        self.p_4 = None
        self.p_5 = None
        self.p_6 = None
        self.p_7 = None
        self.p_8 = None

    @property
    def waterside(self) -> List[Point]:
        return [
            self.p_1,
            self.p_2,
            self.p_3,
            self.p_4,
        ]

    @waterside.setter
    def waterside(self, points: List[Point]):
        if not points or len(points) != 4:
            raise ValueError("Exactly 4 points should be given")
        if not all(isinstance(p, Point) for p in points):
            raise ValueError(f"All points given should be of type {type(Point)}")

        self.p_1 = points[0]
        self.p_2 = points[1]
        self.p_3 = points[2]
        self.p_4 = points[3]

    @property
    def polderside(self) -> List[Point]:
        return [
            self.p_5,
            self.p_6,
            self.p_7,
            self.p_8,
        ]

    @polderside.setter
    def polderside(self, points: List[Point]):
        if not points or len(points) != 4:
            raise ValueError("Exactly 4 points should be given")
        if not all(isinstance(p, Point) for p in points):
            raise ValueError(f"All points given should be of type {type(Point)}")

        self.p_5 = points[0]
        self.p_6 = points[1]
        self.p_7 = points[2]
        self.p_8 = points[3]

    @property
    def points(self) -> List[Point]:
        _points = []
        _points.extend(self.waterside)
        _points.extend(self.polderside)
        return _points

    @property
    def points_data(self) -> List[Tuple[float]]:
        return [(p.x, p.y) for p in self.points]
