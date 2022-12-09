from typing import List, Union

from shapely import affinity, geometry, ops


def as_unified_geometry(
    source_geom: Union[geometry.Polygon, geometry.MultiPolygon]
) -> geometry.Polygon:
    if isinstance(source_geom, geometry.MultiPolygon):
        return source_geom.union(source_geom.convex_hull)
    return source_geom


def get_relative_core_layer(
    core_geometry: geometry.Polygon, coating_geometry: geometry.Polygon
) -> geometry.Polygon:
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
    _aux_coord = geometry.Point(_coating_points[0][0], _core_points[1][1])
    _wrapper_points = geometry.LineString(
        [
            _coating_points[0],
            _aux_coord,
            _core_points[1],
            _core_points[0],
            _coating_points[0],
        ]
    )
    _wrapper_polygon = geometry.Polygon(_wrapper_points)
    _fixed_layer_geom = _wrapper_polygon.intersection(coating_geometry)
    return as_unified_geometry(_fixed_layer_geom.union(core_geometry))


def get_polygon_coordinates(
    pol_geometry: Union[geometry.Polygon, geometry.MultiPolygon]
) -> Union[geometry.LineString, geometry.MultiLineString]:
    if isinstance(pol_geometry, geometry.Polygon):
        return geometry.LineString(pol_geometry.exterior.coords)
    elif isinstance(pol_geometry, geometry.MultiPolygon):
        _geoms_coords = [_geom.exterior.coords for _geom in pol_geometry.geoms]
        return ops.linemerge(_geoms_coords)
    raise NotImplementedError(f"Geometry type {geometry.geom_type} not supported.")


def get_groundlevel_surface(pol_geometry: geometry.Polygon) -> geometry.LineString:
    def _in_groundlevel(geom_coord: geometry.Point) -> bool:
        return geom_coord.y == 0

    return geometry.LineString(
        list(set(filter(_in_groundlevel, get_polygon_coordinates(pol_geometry))))
    )


def _get_single_polygon_surface_points(
    base_geometry: geometry.Polygon,
) -> geometry.LineString:
    _coordinates = list(get_polygon_coordinates(base_geometry).coords)
    if not _coordinates:
        return geometry.LineString()

    _coordinates.pop(-1)
    _x_coords, _ = list(zip(*_coordinates))
    _idx_mlc = _x_coords.index(min(_x_coords))
    _idx_mrc = _x_coords.index(max(_x_coords))
    if _idx_mlc > _idx_mrc:
        _surface_points = _coordinates[: (_idx_mrc + 1)] + _coordinates[_idx_mlc:]
        _surface_points.reverse()
    else:
        _surface_points = _coordinates[_idx_mlc : (_idx_mrc + 1)]

    return geometry.LineString(_surface_points)


def get_polygon_surface_points(
    base_geometry: Union[geometry.Polygon, geometry.MultiPolygon]
) -> geometry.LineString:
    if isinstance(base_geometry, geometry.MultiPolygon):
        return ops.linemerge(
            list(map(_get_single_polygon_surface_points, base_geometry.geoms))
        )
    return _get_single_polygon_surface_points(base_geometry)


def points_to_polygon(points_list: List[geometry.Point]) -> geometry.Polygon:
    _geometry_points = []
    _geometry_points.extend(points_list)
    _geometry_points.append(points_list[0])
    return geometry.Polygon(_geometry_points)


def remove_layer_from_polygon(
    dike_polygon: geometry.Polygon, layer_depth: float
) -> geometry.Polygon:
    _shift_y_geom = affinity.translate(dike_polygon, yoff=-layer_depth)
    return dike_polygon.difference(_shift_y_geom)
