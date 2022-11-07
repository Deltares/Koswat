from typing import List, Union

from shapely.geometry import LineString, MultiPolygon, Point, Polygon


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


def get_polygon_coordinates(geometry: Union[Polygon, MultiPolygon]) -> LineString:
    if geometry.geom_type.lower() == "polygon":
        return LineString(geometry.boundary.coords)
    elif geometry.geom_type.lower() == "multipolygon":
        raise NotImplementedError(f"Geometry type {geometry.geom_type} not supported.")
    raise NotImplementedError(f"Geometry type {geometry.geom_type} not supported.")


def get_polygon_surface_points(
    base_geometry: Union[Polygon, MultiPolygon]
) -> LineString:
    _coordinates = list(get_polygon_coordinates(base_geometry).coords)
    _coordinates.pop(-1)
    _x_coords, _ = list(zip(*_coordinates))
    _idx_mlc = _x_coords.index(min(_x_coords))
    _idx_mrc = _x_coords.index(max(_x_coords))
    if _idx_mlc > _idx_mrc:
        _surface_points = _coordinates[: (_idx_mrc + 1)] + _coordinates[_idx_mlc:]
        _surface_points.reverse()
    else:
        _surface_points = _coordinates[_idx_mlc : (_idx_mrc + 1)]

    return LineString(_surface_points)
