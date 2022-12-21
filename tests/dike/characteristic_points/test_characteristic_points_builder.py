import math

import pytest

from koswat.core.protocols import BuilderProtocol
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
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
        _builder = CharacteristicPointsBuilder()
        _builder.input_profile = InputProfileCases.default
        _expected_points = InitialPointsLookup.default

        # 2. Run test.
        _char_points = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_char_points, CharacteristicPoints)
        for c_idx, c_point in enumerate(_char_points.points):
            assert c_point.almost_equals(_expected_points[c_idx])

    def test_build_waterside(self):
        # 1. Define data.
        _tolerance = 0.001
        _p4_x_coord = 2
        _builder = CharacteristicPointsBuilder()
        _builder.input_profile = InputProfileCases.profile_case_2
        _expected_points = InitialPointsLookup.calc_profile_scenario_2[:4]

        # 2. Run test.
        _char_points = _builder._build_waterside(_p4_x_coord)

        # 3. Verify expectations.
        assert _char_points
        for c_idx, c_point in enumerate(_char_points):
            assert c_point.almost_equals(_expected_points[c_idx], _tolerance)

    def test_build_polderside(self):
        # 1. Define data.
        _p4_x_coord = 2
        _tolerance = 0.001
        _builder = CharacteristicPointsBuilder()
        _builder.input_profile = InputProfileCases.profile_case_2
        _expected_points = InitialPointsLookup.calc_profile_scenario_2[4:]

        # 2. Run test.
        _char_points = _builder._build_polderside(_p4_x_coord)

        # 3. Verify expectations.
        assert _char_points
        for c_idx, c_point in enumerate(_char_points):
            assert c_point.almost_equals(_expected_points[c_idx], _tolerance)

    def test_build_without_input_data_raises_value_error(self):
        with pytest.raises(ValueError) as exc_err:
            CharacteristicPointsBuilder().build()

        assert str(exc_err.value) == "Input Profile should be provided."
