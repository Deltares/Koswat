from __future__ import annotations

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_layers import KoswatLayers
from koswat.profiles.koswat_profile import KoswatProfile
from koswat.profiles.polderside import Polderside
from koswat.profiles.waterside import Waterside


class KoswatProfileBuilder:
    input_profile: KoswatInputProfile
    layers: KoswatLayers

    def __init__(self) -> None:
        self.input_profile = None
        self.layers = None

    def build(self) -> KoswatProfile:
        if not isinstance(self.input_profile, KoswatInputProfile):
            raise ValueError("Koswat Input Profile required.")
        if not isinstance(self.layers, KoswatLayers):
            raise ValueError("Koswat Layers required.")

        _profile = KoswatProfile()
        _profile.input_data = self.input_profile
        _profile.layers = self.layers
        _profile.waterside = Waterside.from_input_profile(self.input_profile)
        _profile.polderside = Polderside.from_input_profile(self.input_profile)
        return _profile

    @classmethod
    def with_data(
        cls, input_profile: KoswatInputProfile, layers: KoswatLayers
    ) -> KoswatProfileBuilder:
        _builder = cls()
        _builder.input_profile = input_profile
        _builder.layers = layers
        return _builder
