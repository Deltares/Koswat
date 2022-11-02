from typing import List

from shapely import affinity, geometry


def points_to_polygon(points_list: List[geometry.Point]) -> geometry.Polygon:
    _geometry_points = []
    _geometry_points.extend(points_list)
    _geometry_points.append(points_list[0])
    return geometry.Polygon(_geometry_points)


def remove_layer_from_polygon(
    dike_polygon: geometry.Polygon, layer_depth: float
) -> geometry.Polygon:
    _shift_y_geom = affinity.translate(dike_polygon, yoff=-layer_depth)
    _shift_y_geom = dike_polygon.intersection(_shift_y_geom)
    _shift_x = affinity.translate(dike_polygon, xoff=-layer_depth)
    _shift_x = _shift_x.intersection(affinity.translate(dike_polygon, xoff=layer_depth))
    return _shift_y_geom
