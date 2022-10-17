from __future__ import annotations

import math
from typing import Optional, Type

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_layers import KoswatLayers
from koswat.dike.layers.koswat_layers_builder import KoswatLayersBuilder
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class KoswatProfileBuilder(BuilderProtocol):
    input_profile_data: dict
    layers_data: dict
    p4_x_coordinate: Optional[float]
    profile_type: Type[KoswatProfileProtocol]

    def __init__(self) -> None:
        self.input_profile_data = {}
        self.layers_data = {}
        self.p4_x_coordinate = math.nan
        self.profile_type = None

    def _build_characteristic_points(
        self, input_profile: KoswatInputProfileBase
    ) -> CharacteristicPoints:
        _char_points_builder = CharacteristicPointsBuilder()
        _char_points_builder.input_profile = input_profile
        if math.isnan(self.p4_x_coordinate):
            self.p4_x_coordinate = 0
        _char_points_builder.p4_x_coordinate = self.p4_x_coordinate
        return _char_points_builder.build()

    def _build_layers(self, profile_points: CharacteristicPoints) -> KoswatLayers:
        _layers_builder = KoswatLayersBuilder()
        _layers_builder.layers_data = self.layers_data
        _layers_builder.profile_points = profile_points.points
        return _layers_builder.build()

    def build(self) -> KoswatProfileProtocol:
        if not isinstance(self.input_profile_data, dict):
            raise ValueError("Koswat Input Profile data dictionary required.")
        if not isinstance(self.layers_data, dict):
            raise ValueError("Koswat Layers data dictionary required.")
        if not (self.profile_type and issubclass(self.profile_type, KoswatProfileBase)):
            raise ValueError(
                f"Koswat profile type should be a concrete class of {KoswatProfileBase.__name__}."
            )

        _profile = self.profile_type()
        _profile.input_data = KoswatInputProfileBase.from_dict(self.input_profile_data)
        _profile.characteristic_points = self._build_characteristic_points(
            _profile.input_data
        )
        _profile.layers_wrapper = self._build_layers(_profile.characteristic_points)
        return _profile

    @classmethod
    def with_data(
        cls,
        builder_data: dict,
    ) -> KoswatProfileBuilder:
        _builder = cls()
        _builder.input_profile_data = builder_data["input_profile_data"]
        _builder.layers_data = builder_data["layers_data"]
        _builder.p4_x_coordinate = builder_data.get("p4_x_coordinate", 0)
        _builder.profile_type = builder_data.get("profile_type", KoswatProfileBase)
        return _builder
