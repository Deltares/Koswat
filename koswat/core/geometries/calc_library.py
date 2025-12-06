"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging

from shapely import affinity, geometry, ops


def order_geometry_points(dike_polygon: geometry.Polygon) -> geometry.Polygon:
    """
    In koswat we handle polygon operations expecting the lowest 'x' coordinate to be the initial and last point of a geometry.
    For this reason we need to ensure all geometries are 'normalized' based on this criteria.

    Args:
        dike_polygon (geometry.Polygon): Polygon to normalized.

    Returns:
        geometry.Polygon: Normalized polygon.
    """
    if isinstance(dike_polygon.boundary, geometry.MultiLineString):
        logging.warning(
            "Polygon with 'multi line', most likely due to a geometry split in two parts. Ordering of points is not supported, some calculation errors might occur as a consequence of this."
        )
        return dike_polygon
    _x, _y = tuple(map(list, dike_polygon.boundary.coords.xy))
    # remove last point as it's repeated.
    _x.pop(-1)
    _y.pop(-1)
    _lowest_x = _x.index(min(_x))
    if _lowest_x == 0:
        # It's already in ordered.
        return dike_polygon
    # We can assume that there won't be two 'lowest' x points with different y position (so a 'cliff')
    new_x = _x[_lowest_x:] + _x[0:_lowest_x] + [_x[_lowest_x]]
    new_y = _y[_lowest_x:] + _y[0:_lowest_x] + [_y[_lowest_x]]
    _points = [(new_x[idx], new_y[idx]) for idx in range(0, len(new_x))]
    return geometry.Polygon(_points)


def as_unified_geometry(
    source_geom: geometry.Polygon | geometry.MultiPolygon,
) -> geometry.Polygon:
    """
    Ensures the calculated geometry is returned as a single polygon.

    Args:
        source_geom (geometry.Polygon | geometry.MultiPolygon): Calculated source geometry.

    Returns:
        geometry.Polygon: Unified resulting geometry with its points ordered (first one is the most-left x coordinate).
    """
    if isinstance(source_geom, geometry.MultiPolygon):
        return order_geometry_points(source_geom.union(source_geom.convex_hull))
    return order_geometry_points(source_geom)


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
    pol_geometry: geometry.Polygon | geometry.MultiPolygon,
) -> geometry.LineString:
    """
    Given a single or multi geometry returns the coordinates composing its outer layout.

    Args:
        pol_geometry (geometry.Polygon | geometry.MultiPolygon): Source geometry.

    Raises:
        NotImplementedError: When the provided geometry is not yet supported.

    Returns:
        geometry.LineString: Set of points composing the outer layout of the geometry.
    """
    if isinstance(pol_geometry, geometry.Polygon):
        return geometry.LineString(pol_geometry.exterior.coords)
    raise NotImplementedError(f"Geometry type {pol_geometry.geom_type} not supported.")


def get_groundlevel_surface(pol_geometry: geometry.Polygon) -> geometry.LineString:
    """
    Returns all the points which are at 'groundlevel' values (y = 0)

    Args:
        pol_geometry (geometry.Polygon): Source geometry.

    Returns:
        geometry.LineString: Line with points at y = 0.
    """

    def _in_groundlevel(geom_coord: geometry.Point) -> bool:
        return geom_coord.y == 0

    return geometry.LineString(
        list(set(filter(_in_groundlevel, get_polygon_coordinates(pol_geometry))))
    )


def _get_normalized_polygon(base_polygon: geometry.Polygon) -> geometry.Polygon:
    _coordinates = list(get_polygon_coordinates(base_polygon).coords)
    if not _coordinates:
        return geometry.LineString()
    _coordinates.pop(-1)

    def _last_point_intersects() -> bool:
        if _coordinates[1][0] <= _coordinates[-1][0]:
            return False
        _gls = geometry.LineString(_coordinates[0:2])
        return _gls.intersects(geometry.Point(_coordinates[-1]).buffer(0.01))

    while _last_point_intersects():
        # Apparently sometimes the difference method does not entirely take out the water-side old polygon for a very small precision difference.
        _coordinates.pop(0)
        _coordinates.insert(0, _coordinates.pop(-1))
    _coordinates.append(_coordinates[0])
    return geometry.Polygon(_coordinates)


def get_normalized_polygon_difference(
    left_geom: geometry.Polygon, right_geom: geometry.Polygon
) -> geometry.Polygon | geometry.MultiPolygon:
    """
    Given two polygons calculates the difference between them and removes any residual polygon due to minor precision errors.

    Args:
        left_geom (geometry.Polygon): Base polygon from where to substract.
        right_geom (geometry.Polygon): Polygon to substract from base.

    Returns:
        geometry.Polygon: Resulting normalized substraction polygon.
    """
    _result_geom = left_geom.difference(right_geom)
    if isinstance(_result_geom, geometry.MultiPolygon):
        # Try to filter out sliver polygons caused by precision issues.
        _result_geom = ops.unary_union([p for p in _result_geom.geoms if p.area > 0.1])
        if isinstance(_result_geom, geometry.MultiPolygon):
            return geometry.MultiPolygon(
                map(_get_normalized_polygon, _result_geom.geoms)
            )
    return _get_normalized_polygon(order_geometry_points(_result_geom))


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
        _surface_points = _coordinates[_idx_mlc:] + _coordinates[: (_idx_mrc + 1)]
    else:
        _surface_points = _coordinates[_idx_mlc : (_idx_mrc + 1)]

    return geometry.LineString(_surface_points)


def get_polygon_surface_points(
    base_geometry: geometry.Polygon | geometry.MultiPolygon,
) -> geometry.LineString:
    """
    Gets all the points composing the upper surface of a 'dike' geometry.
    IMPORTANT! The calling of this method __assumes__ the `base_geometry` points are in order, call `order_geometry_points` if needed.

    Args:
        base_geometry (Union[geometry.Polygon, geometry.MultiPolygon]): Source geometry.

    Returns:
        geometry.LineString: Resulting line with points from the outer geometry.
    """
    if isinstance(base_geometry, geometry.MultiPolygon):
        return ops.linemerge(
            list(map(_get_single_polygon_surface_points, base_geometry.geoms))
        )
    if isinstance(base_geometry, geometry.Polygon):
        return _get_single_polygon_surface_points(base_geometry)
    return base_geometry


def profile_points_to_polygon(points_list: list[geometry.Point]) -> geometry.Polygon:
    """
    Transforms a list of points into a valid 'dike' polygon. When there is a difference in height between left and right side then we correct it in the x = 0 coordinate.

    Args:
        points_list (List[geometry.Point]): List of points representing a dike profile.

    Returns:
        geometry.Polygon: Validated enclosed geometry simple polygon.
    """
    _geometry_points = []
    _geometry_points.extend(points_list)
    if points_list[0].y != points_list[-1].y:
        _geometry_points.append(geometry.Point(0, points_list[-1].y))
        _geometry_points.append(geometry.Point(0, points_list[0].y))
    _geometry_points.append(points_list[0])
    return geometry.Polygon(geometry.LineString(_geometry_points))


def remove_layer_from_polygon(
    dike_polygon: geometry.Polygon, layer_depth: float
) -> geometry.Polygon:
    """
    Gets the dike profile without a layer of provided `layer_depth` depth.

    Args:
        dike_polygon (geometry.Polygon): Source geometry.
        layer_depth (float): Depth of a layer from the outer `dike_polygon` geometry inwards.

    Returns:
        geometry.Polygon: Resulting geometry when removing the layer.
    """
    _shift_y_geom = affinity.translate(dike_polygon, yoff=-layer_depth)
    return dike_polygon.difference(_shift_y_geom)
