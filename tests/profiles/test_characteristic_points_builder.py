import math

import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.profiles.characteristic_points import CharacteristicPoints
from koswat.profiles.characteristic_points_builder import CharacteristicPointsBuilder
from tests.library_test_cases import InitialPointsLookup, InputProfileCases


class TestCharacteristicPointsBuilder:
    def test_initialize(self):
        _builder = CharacteristicPointsBuilder()
        assert isinstance(_builder, CharacteristicPointsBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.input_profile
        assert math.isnan(_builder.p4_x_coordinate)

    def test_build_without_p4_x_coordinate(self):
        # 1. Define data.
        _input_data = InputProfileCases.default
        _builder = CharacteristicPointsBuilder()
        _builder.input_profile = _input_data
        _expected_points = InitialPointsLookup.default

        # 2. Run test.
        _char_points = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_char_points, CharacteristicPoints)
        for c_idx, c_point in enumerate(_char_points.points):
            assert c_point.almost_equals(_expected_points[c_idx])

    def test_build_without_input_data_raises_value_error(self):
        with pytest.raises(ValueError) as exc_err:
            CharacteristicPointsBuilder().build()

        assert str(exc_err.value) == "Input Profile should be provided."
