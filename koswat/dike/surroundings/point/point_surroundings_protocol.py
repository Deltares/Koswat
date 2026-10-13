from shapely import Point


class PointSurroundingsProtocol:
    section: str
    traject_order: int
    location: Point | None
