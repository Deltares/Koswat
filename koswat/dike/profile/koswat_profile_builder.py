"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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

from __future__ import annotations

import math
from typing import Optional

from koswat.core.protocols import BuilderProtocol
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.layers_wrapper import (
    KoswatLayersWrapper,
    KoswatLayersWrapperBuilder,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class KoswatProfileBuilder(BuilderProtocol):
    input_profile_data: KoswatInputProfileBase
    layers_data: dict
    p4_x_coordinate: Optional[float]

    def __init__(self) -> None:
        self.input_profile_data = None
        self.layers_data = {}
        self.p4_x_coordinate = math.nan

    def _build_characteristic_points(
        self, input_profile: KoswatInputProfileBase
    ) -> CharacteristicPoints:
        _char_points_builder = CharacteristicPointsBuilder()
        _char_points_builder.input_profile = input_profile
        if math.isnan(self.p4_x_coordinate):
            self.p4_x_coordinate = 0
        _char_points_builder.p4_x_coordinate = self.p4_x_coordinate
        return _char_points_builder.build()

    def _build_layers(
        self, profile_points: CharacteristicPoints
    ) -> KoswatLayersWrapper:
        _layers_builder = KoswatLayersWrapperBuilder()
        _layers_builder.layers_data = self.layers_data
        _layers_builder.profile_points = profile_points.points
        return _layers_builder.build()

    def build(self) -> KoswatProfileProtocol:
        if not isinstance(self.input_profile_data, KoswatInputProfileBase):
            raise ValueError("Koswat Input Profile data instance required.")
        if not isinstance(self.layers_data, dict):
            raise ValueError("Koswat Layers data dictionary required.")

        _profile = KoswatProfileBase()
        _profile.input_data = self.input_profile_data
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
        return _builder
