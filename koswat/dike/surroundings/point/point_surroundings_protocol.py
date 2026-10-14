from shapely import Point


class PointSurroundingsProtocol:
    """
    Protocol for classes describing the surroundings on a certain point.
    """

    section: str
    traject_order: int
    location: Point
