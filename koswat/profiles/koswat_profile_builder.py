from __future__ import annotations

from email.mime import base
from typing import List

from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_layers import KoswatLayer, KoswatLayers
from koswat.profiles.koswat_material import KoswatMaterialFactory
from koswat.profiles.koswat_profile import KoswatProfile
from koswat.profiles.polderside import Polderside
from koswat.profiles.waterside import Waterside


class KoswatLayersBuilder:
    layers_data: dict
    profile_points: List[Point]

    def _build_base_geometry(self, layer_data: dict) -> KoswatLayer:
        _geometry_points = []
        _geometry_points.extend(self.profile_points)
        _geometry_points.append(self.profile_points[0])
        _layer = KoswatLayer()
        _layer.geometry = Polygon(_geometry_points)
        _layer.material = KoswatMaterialFactory.get_material(layer_data["material"])
        return _layer

    def _build_coating_layer(
        self, base_geometry: Polygon, layer_data: dict
    ) -> KoswatLayer:
        _depth = layer_data["depth"]
        _layer = KoswatLayer()
        # TODO
        # _layer.geometry = ??
        _layer.material = KoswatMaterialFactory.get_material(layer_data["material"])
        return _layer

    def build(self) -> KoswatLayers:
        _layers = KoswatLayers()
        _layers.base_layer = self._build_base_geometry(self.layers_data["base_layer"])
        _layers.coating_layers = [
            self._build_coating_layer(_layers.base_layer.geometry, c_layer)
            for c_layer in self.layers_data["coating_layers"]
        ]
        return _layers


class KoswatProfileBuilder:
    input_profile_data: dict
    layers_data: dict

    def __init__(self) -> None:
        self.input_profile = None
        self.layers = None

    def build(self) -> KoswatProfile:
        if not isinstance(self.input_profile, dict):
            raise ValueError("Koswat Input Profile data dictionary required.")
        if not isinstance(self.layers, dict):
            raise ValueError("Koswat Layers data dictionary required.")

        _profile = KoswatProfile()
        _profile.waterside = Waterside.from_input_profile(self.input_profile)
        _profile.polderside = Polderside.from_input_profile(self.input_profile)
        _profile.input_data = self.input_profile
        _profile.layers = self.build_layers(_profile.points)
        return _profile

    @classmethod
    def with_data(cls, input_profile_data: dict, layers: dict) -> KoswatProfileBuilder:
        _builder = cls()
        _builder.input_profile = KoswatInputProfile.from_dict(input_profile_data)
        _builder.layers = layers
        return _builder
