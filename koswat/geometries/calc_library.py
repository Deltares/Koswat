from shapely.geometry import LineString, Point, Polygon


def get_relative_core_layer(
    core_geometry: Polygon, coating_geometry: Polygon
) -> Polygon:
    """
    Returns a new 'core' from the original `core_geometry` relative to the `coating_geometry`.

    Args:
        core_geometry (Polygon): Original core geometry on which layers are stacked upon.
        coating_geometry (Polygon): Layer wrapping the exterior of a core geometry.

    Returns:
        Polygon: Layer wrapping a reduced surface of the `core_geometry`.
    """
    # Create a 'fake' base layer geometry to later do proper intersections.
    _core_points = list(core_geometry.boundary.coords)
    _coating_points = list(coating_geometry.boundary.coords)
    _aux_coord = Point(_coating_points[0][0], _core_points[1][1])
    _wrapper_points = LineString(
        [
            _coating_points[0],
            _aux_coord,
            _core_points[1],
            _core_points[0],
            _coating_points[0],
        ]
    )
    _wrapper_polygon = Polygon(_wrapper_points)
    _fixed_layer_geom = _wrapper_polygon.intersection(coating_geometry)
    return _fixed_layer_geom.union(core_geometry)
