import pytest

from koswat.configuration.io.csv.koswat_simple_surroundings_csv_reader import KoswatSimpleSurroundingsCsvReader
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.dike.surroundings.point.point_obstacle_surroundings import PointObstacleSurroundings
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

    def test_when_build_point_surroundings_then_reduced_surroundings_matrix(
        self
    ):
        # 1. Define test data.
        _section = "Dummy"
        _traject_order = -1
        _location_x = 4.2
        _location_y = 2.4
        distance_weights = [500, 200, 0, 0]

        # 2. Run test.
        _point_surroundings = KoswatSimpleSurroundingsCsvReader()._build_point_surroundings(
            entry=[
                _traject_order,
                _section,
                _location_x,
                _location_y,
                *distance_weights,
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
        assert _point_surroundings.inside_distance == 500
        assert _point_surroundings.outside_distance == 200
        assert _point_surroundings.angle_inside == 0
        assert _point_surroundings.angle_outside == 0
        assert _point_surroundings.closest_obstacle == _point_surroundings.inside_distance
