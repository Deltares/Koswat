from typing import Optional

import pytest

from koswat.configuration.io.csv.koswat_simple_surroundings_csv_reader import (
    KoswatSimpleSurroundingsCsvReader,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.dike.surroundings.point.point_obstacle_surroundings import (
    PointObstacleSurroundings,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from tests import test_data


class TestKoswatSimpleSurroundingsCsvReader:
    def test_initialize(self):
        _csv_reader = KoswatSimpleSurroundingsCsvReader()
        assert isinstance(_csv_reader, KoswatSimpleSurroundingsCsvReader)
        assert isinstance(_csv_reader, KoswatReaderProtocol)

    def test_read_given_valid_file(self):
        # 1. Define test data
        _reader = KoswatSimpleSurroundingsCsvReader()
        _test_file = test_data.joinpath(
            "csv_reader", "Omgeving", "T_10_3_bebouwing.csv"
        )
        assert _test_file.is_file()

        # 2. Run test.
        _csv_fom = _reader.read(_test_file)

        # 3. Verify expectations.
        assert isinstance(_csv_fom, KoswatSurroundingsCsvFom)
        assert _csv_fom.is_valid()

    @pytest.mark.parametrize(
        "given_surroundings_buffer, expected_applied_surroundings_buffer",
        [
            pytest.param(0.0, 0.0, id="Zero buffer"),
            pytest.param(10.0, 10.0, id="Non-zero buffer"),
            pytest.param(-5.0, 0.0, id="Negative buffer"),
            pytest.param(None, 0.0, id="None buffer"),
        ],
    )
    def test_when_build_point_surroundings_then_reduced_surroundings_matrix(
        self,
        given_surroundings_buffer: Optional[float],
        expected_applied_surroundings_buffer: float,
    ):
        # 1. Define test data.
        _section = "Dummy"
        _traject_order = -1
        _location_x = 4.2
        _location_y = 2.4
        _expected_inside_distance = 500 - expected_applied_surroundings_buffer
        _expected_outside_distance = 200 - expected_applied_surroundings_buffer
        _distance_weights = [500, 200, 0, 0]

        # 2. Run test.
        _reader = KoswatSimpleSurroundingsCsvReader()
        _reader.surroundings_buffer = given_surroundings_buffer
        _point_surroundings = _reader._build_point_surroundings(
            entry=[
                _traject_order,
                _section,
                _location_x,
                _location_y,
                *_distance_weights,
            ],
        )

        # 3. Verify expectations.
        assert isinstance(_point_surroundings, PointSurroundings)
        assert isinstance(_point_surroundings, PointObstacleSurroundings)
        assert _point_surroundings.section == _section
        assert _point_surroundings.traject_order == _traject_order
        assert _point_surroundings.location.x == _location_x
        assert _point_surroundings.location.y == _location_y
        assert _point_surroundings.surroundings_matrix == []
        assert _point_surroundings.inside_distance == _expected_inside_distance
        assert _point_surroundings.outside_distance == _expected_outside_distance
        assert _point_surroundings.angle_inside == 0
        assert _point_surroundings.angle_outside == 0
