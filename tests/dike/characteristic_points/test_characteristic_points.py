from typing import Callable, List, Optional

import pytest
from shapely.geometry import Point

from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints


def set_polderside(char_points: CharacteristicPoints, points: Optional[List[Point]]):
    char_points.polderside = points


def set_waterside(char_points: CharacteristicPoints, points: Optional[List[Point]]):
    char_points.waterside = points


class TestCharacteristicPoints:
    def test_initialize(self):
        _char_points = CharacteristicPoints()
        assert isinstance(_char_points, CharacteristicPoints)
        assert _char_points.points == [None] * 8
        assert _char_points.waterside == [None] * 4
        assert _char_points.polderside == [None] * 4

    _wrong_number_of_points = "Exactly 4 points should be given"
    _wrong_points_type = f"All points given should be of type {type(Point)}"

    @pytest.mark.parametrize(
        "side_func",
        [
            pytest.param(set_polderside, id="Polderside"),
            pytest.param(set_waterside, id="Waterside"),
        ],
    )
    @pytest.mark.parametrize(
        "points_to_add, expected_err",
        [
            pytest.param(None, _wrong_number_of_points, id="No points parameter given"),
            pytest.param([], _wrong_number_of_points, id="Not enough points given"),
            pytest.param(
                [None] * 6, _wrong_number_of_points, id="Too many points given"
            ),
            pytest.param([4.2] * 4, _wrong_points_type, id="Points as simple floats"),
            pytest.param(
                [(4.2, 2.4)] * 4, _wrong_points_type, id="Points as float tuples"
            ),
        ],
    )
    def test_add_side_poitns_raises_error_when_exact_points_given(
        self,
        side_func: Callable,
        points_to_add: Optional[List[float]],
        expected_err: str,
    ):
        _char_points = CharacteristicPoints()
        with pytest.raises(ValueError) as exc_err:
            side_func(_char_points, points_to_add)
        assert str(exc_err.value) == expected_err

    def test_add_waterside_points_with_valid_data(self):
        _char_points = CharacteristicPoints()
        _points_to_add = [Point(4.2, 2.4)] * 4
        _char_points.waterside = _points_to_add
        assert _points_to_add == _char_points.waterside
        assert _points_to_add == _char_points.points[:4]

    def test_add_polderside_points_with_valid_data(self):
        _char_points = CharacteristicPoints()
        _points_to_add = [Point(4.2, 2.4)] * 4
        _char_points.polderside = _points_to_add
        assert _points_to_add == _char_points.polderside
        assert _points_to_add == _char_points.points[4:]

    def test_points_returns_both_water_and_polder_side_points(self):
        # 1. Define test data.
        _char_points = CharacteristicPoints()
        _polderside_points = [Point(4.2, 2.4)] * 4
        _waterside_points = [Point(2.4, 4.2)] * 4
        _char_points.polderside = _polderside_points
        _char_points.waterside = _waterside_points

        # 2. Run test
        _expected_points = []
        _expected_points = _waterside_points
        _expected_points.extend(_polderside_points)

        # 3. Verify expectations
        assert _char_points.points == _expected_points
