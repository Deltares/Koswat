from typing import Optional

import pytest

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.dike.surroundings.point.point_obstacle_surroundings import (
    PointObstacleSurroundings,
)


class TestKoswatSurroundingsCsvFom:
    def test_initialize(self):
        _csv_fom = KoswatSurroundingsCsvFom()
        assert isinstance(_csv_fom, KoswatSurroundingsCsvFom)
        assert isinstance(_csv_fom, KoswatCsvFomProtocol)
        assert not _csv_fom.points_surroundings_list
        assert _csv_fom.traject == ""
        assert not _csv_fom.is_valid()

    @pytest.mark.parametrize(
        "buffer",
        [
            None,
            0,
            -1,
        ],
    )
    def test_when_apply_buffer_given_invalid_buffer_then_distance_not_adjusted(
        self, buffer: Optional[float]
    ):
        # 1. Define test data
        _expected_inside_distance = 10.0
        _expected_outside_distance = 15.0
        _csv_fom = KoswatSurroundingsCsvFom(
            points_surroundings_list=[
                PointObstacleSurroundings(
                    inside_distance=_expected_inside_distance,
                    outside_distance=_expected_outside_distance,
                )
            ]
        )

        # 2. Execute test
        _csv_fom.apply_buffer(buffer)

        # 3. Verify expectations
        assert (
            _csv_fom.points_surroundings_list[0].inside_distance
            == _expected_inside_distance
        )
        assert (
            _csv_fom.points_surroundings_list[0].outside_distance
            == _expected_outside_distance
        )

    def test_when_apply_buffer_given_valid_buffer_then_distance_adjusted(
        self,
    ):
        # 1. Define test data
        _buffer = 5.0
        _expected_inside_distance = 10.0 - _buffer
        _expected_outside_distance = 15.0 - _buffer
        _csv_fom = KoswatSurroundingsCsvFom(
            points_surroundings_list=[
                PointObstacleSurroundings(
                    inside_distance=10.0,
                    outside_distance=15.0,
                )
            ]
        )

        # 2. Execute test
        _csv_fom.apply_buffer(_buffer)

        # 3. Verify expectations
        assert (
            _csv_fom.points_surroundings_list[0].inside_distance
            == _expected_inside_distance
        )
        assert (
            _csv_fom.points_surroundings_list[0].outside_distance
            == _expected_outside_distance
        )

    def test_when_merge_given_different_traject_then_raise_exception(self):
        # 1. Define test data
        _csv_fom_1 = KoswatSurroundingsCsvFom(traject="traject_1")
        _csv_fom_2 = KoswatSurroundingsCsvFom(traject="traject_2")

        # 2. Execute test and verify expectations
        with pytest.raises(ValueError):
            _csv_fom_1.merge(_csv_fom_2)

    def test_when_merge_given_same_traject_then_points_merged(
        self,
    ):
        # 1. Define test data
        _csv_fom_1 = KoswatSurroundingsCsvFom(
            points_surroundings_list=[
                PointObstacleSurroundings(
                    location=(0, 0),
                    inside_distance=10.0,
                    outside_distance=15.0,
                )
            ],
            traject="traject_1",
        )
        _csv_fom_2 = KoswatSurroundingsCsvFom(
            points_surroundings_list=[
                PointObstacleSurroundings(
                    location=(0, 0),
                    inside_distance=5.0,
                    outside_distance=10.0,
                ),
                PointObstacleSurroundings(
                    location=(1, 1),
                    inside_distance=8.0,
                    outside_distance=12.0,
                ),
            ],
            traject="traject_1",
        )

        # 2. Execute test
        _csv_fom_1.merge(_csv_fom_2)

        # 3. Verify expectations
        assert len(_csv_fom_1.points_surroundings_list) == 2
        assert all(
            isinstance(_point, PointObstacleSurroundings)
            for _point in _csv_fom_1.points_surroundings_list
        )
        assert _csv_fom_1.points_surroundings_list[0].location == (0, 0)
        assert _csv_fom_1.points_surroundings_list[0].inside_distance == 5.0
        assert _csv_fom_1.points_surroundings_list[0].outside_distance == 10.0
        assert _csv_fom_1.points_surroundings_list[1].location == (1, 1)
        assert _csv_fom_1.points_surroundings_list[1].inside_distance == 8.0
        assert _csv_fom_1.points_surroundings_list[1].outside_distance == 12.0
