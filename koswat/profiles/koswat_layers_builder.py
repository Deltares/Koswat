from __future__ import annotations

import math
from typing import List

from matplotlib import pyplot
from shapely import geometry

from koswat.builder_protocol import BuilderProtocol
from koswat.profiles.koswat_layers import (
    KoswatBaseLayer,
    KoswatCoatingLayer,
    KoswatLayers,
)
from koswat.profiles.koswat_material import KoswatMaterialFactory


def plot_line(ax, ob, color):
    parts = hasattr(ob, "geoms") and ob or [ob]
    for part in parts:
        x, y = part.xy
        ax.plot(x, y, color=color, linewidth=3, solid_capstyle="round", zorder=1)


class KoswatLayersBuilder(BuilderProtocol):
    layers_data: dict = {}
    profile_points: List[geometry.Point] = []
    profile_geometry: geometry.Polygon = None

    def _plot_linestrings(
        self,
        upper_linestring: geometry.LineString,
        lower_linestring: geometry.LineString,
    ) -> None:
        fig = pyplot.figure(1, dpi=90)
        ax = fig.add_subplot(221)
        plot_line(ax, upper_linestring, color="#aaa")
        plot_line(ax, lower_linestring, color="#eee")
        # pyplot.show()

    def _build_base_layer(
        self, upper_layer_linestring: geometry.LineString, layer_data: dict
    ) -> KoswatBaseLayer:
        _material = KoswatMaterialFactory.get_material(layer_data["material"])
        _layer = KoswatBaseLayer()
        _geometry_points = []
        _upper_layer_points = list(upper_layer_linestring.coords)
        _geometry_points.extend(_upper_layer_points)
        _geometry_points.append(_upper_layer_points[0])
        _layer.geometry = geometry.Polygon(_geometry_points)
        _layer.material = _material
        return _layer

    def _build_coating_layer(
        self, upper_layer_linestring: geometry.LineString, layer_data: dict
    ) -> KoswatCoatingLayer:
        _depth = layer_data.get("depth", math.nan)
        _material = KoswatMaterialFactory.get_material(layer_data["material"])
        if math.isnan(_depth):
            # Usually only for the base layer (sand)
            raise ValueError(
                f"Depth cannot be negative in a coating layer. Layer: {_material.name}"
            )

        # Get the offset linestring
        _offset_geom_linestring = upper_layer_linestring.parallel_offset(
            -_depth, side="left", join_style=2
        )
        # We need to cut the 'y' axis as it might have gone below
        _offset_geom_linestring = _offset_geom_linestring.intersection(
            self.profile_geometry
        )
        self._plot_linestrings(upper_layer_linestring, _offset_geom_linestring)
        _offset_geom_coords = list(_offset_geom_linestring.coords)
        if _offset_geom_coords[-1][0] > _offset_geom_coords[0][0]:
            # Reverse it so it can be built into a polygon with the upper layer.
            _offset_geom_coords.reverse()
        # Avoid duplicates while preserving order
        _layer_geometry_points = list(dict.fromkeys(upper_layer_linestring.coords))
        _layer_geometry_points.extend(_offset_geom_coords)
        _layer_geometry_points.append(_layer_geometry_points[0])
        _offset_geom_coords.reverse()

        # Create the new coating layer
        _layer = KoswatCoatingLayer()
        _layer.layer_points = geometry.LineString(_offset_geom_coords)
        _layer.geometry = geometry.Polygon(_layer_geometry_points)
        _layer.material = _material
        _layer.depth = _depth
        return _layer

    def _set_profile_geometry(self):
        _geometry_points = []
        _geometry_points.extend(self.profile_points)
        _geometry_points.append(self.profile_points[0])
        self.profile_geometry = geometry.Polygon(_geometry_points)

    def build(self) -> KoswatLayers:
        _koswat_layers = KoswatLayers()
        _koswat_layers.coating_layers = []
        if not self.profile_geometry:
            self._set_profile_geometry()
        _parent_points = geometry.LineString(self.profile_points)
        for c_layer_data in self.layers_data.get("coating_layers", []):
            _c_layer = self._build_coating_layer(_parent_points, c_layer_data)
            _parent_points = _c_layer.layer_points
            _koswat_layers.coating_layers.append(_c_layer)
        _koswat_layers.base_layer = self._build_base_layer(
            _parent_points, self.layers_data["base_layer"]
        )
        return _koswat_layers

    @staticmethod
    def layers_as_dict(layers: KoswatLayers) -> dict:
        _base_layer = dict(material=layers.base_layer.material.name, depth=math.nan)
        # TODO: Logic for coating layers.
        return dict(base_layer=_base_layer, coating_layers=dict())
