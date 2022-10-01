from __future__ import annotations

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_layers import KoswatLayers
from koswat.profiles.koswat_layers_builder import KoswatLayersBuilder
from koswat.profiles.koswat_profile import KoswatProfile
from koswat.profiles.polderside import Polderside
from koswat.profiles.waterside import Waterside


class KoswatProfileBuilder:
    input_profile_data: dict = {}
    layers_data: dict = {}

    def build(self) -> KoswatProfile:
        if not isinstance(self.input_profile_data, dict):
            raise ValueError("Koswat Input Profile data dictionary required.")
        if not isinstance(self.layers_data, dict):
            raise ValueError("Koswat Layers data dictionary required.")

        _profile = KoswatProfile()
        _input_data = KoswatInputProfile.from_dict(self.input_profile_data)
        _profile.waterside = Waterside.from_input_profile(_input_data)
        _profile.polderside = Polderside.from_input_profile(_input_data)
        _profile.input_data = _input_data
        _layers_builder = KoswatLayersBuilder()
        _layers_builder.layers_data = self.layers_data
        _layers_builder.profile_points = _profile.points
        _profile.layers = _layers_builder.build()
        return _profile

    @classmethod
    def with_data(
        cls, input_profile_data: dict, layers_data: dict
    ) -> KoswatProfileBuilder:
        _builder = cls()
        _builder.input_profile_data = input_profile_data
        _builder.layers_data = layers_data
        return _builder
