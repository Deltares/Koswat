from shapely.geometry.point import Point

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_layers import KoswatLayers
from koswat.profiles.koswat_profile import KoswatProfile
from koswat.profiles.koswat_profile_builder import KoswatProfileBuilder
from koswat.profiles.polderside import Polderside
from koswat.profiles.waterside import Waterside
from tests.profiles.input_profile_cases import default_case


class TestKoswatProfileBuilder:
    def test_initialize_init_(self):
        _builder = KoswatProfileBuilder()
        assert isinstance(_builder, KoswatProfileBuilder)
        assert not _builder.input_profile
        assert not _builder.layers

    def test_initialized_with_data(self):
        # 1. Define test data.
        assert isinstance(default_case, KoswatInputProfile)
        _layers = KoswatLayers()

        # 2. Run test.
        _profile_builder = KoswatProfileBuilder.with_data(default_case, _layers)

        # 3. Verify final expectations.
        assert isinstance(_profile_builder, KoswatProfileBuilder)
        assert isinstance(_profile_builder.input_profile, KoswatInputProfile)
        assert _profile_builder.input_profile == default_case
        assert isinstance(_profile_builder.layers, KoswatLayers)
        assert _profile_builder.layers == _layers

    def test_given_valid_data_when_build_returns_profile(self):
        # 1. Define test data.
        assert isinstance(default_case, KoswatInputProfile)
        _layers = KoswatLayers()

        # 2. Run test.
        _profile_builder = KoswatProfileBuilder()
        _profile_builder.input_profile = default_case
        _profile_builder.layers = _layers
        _koswat_profile = _profile_builder.build()

        # 3. Verify final expectations.
        assert isinstance(_koswat_profile, KoswatProfile)
        assert _koswat_profile.input_data == default_case
        assert _koswat_profile.layers == _layers
        assert isinstance(_koswat_profile.waterside, Waterside)
        assert isinstance(_koswat_profile.polderside, Polderside)
