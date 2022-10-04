from typing import List

import pytest
from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.io.koswat_csv_fom import KoswatCsvFomBuilder, PointSurroundings
from koswat.io.koswat_csv_reader import KoswatCsvFom
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class TestPointSurroundings:
    def test_initialize_point_surroundings(self):
        _p_s = PointSurroundings()
        assert isinstance(_p_s, PointSurroundings)
        assert isinstance(_p_s, FileObjectModelProtocol)
        assert not _p_s.section
        assert not _p_s.location
        assert not _p_s.distance_to_buildings
        assert not _p_s.is_valid()


class TestKoswatCsvFom:
    def test_initialize_koswat_csv_fom(self):
        _csv_fom = KoswatCsvFom()
        assert isinstance(_csv_fom, KoswatCsvFom)
        assert isinstance(_csv_fom, FileObjectModelProtocol)
        assert not _csv_fom.points_surroundings_list
        assert not _csv_fom.is_valid()


class TestKoswatCsvFomBuilder:
    def test_initialize_koswat_csv_fom_builder(self):
        _builder = KoswatCsvFomBuilder()
        assert isinstance(_builder, KoswatCsvFomBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.headers
        assert not _builder.entries
        assert not _builder._is_valid()

    def test_given_headers_and_entries_returns_koswat_fom(self):
        # 1. Define test data.
        _headers = ["a_section", "x_coord", "y_coord", "afst_24m", "afst_42m"]
        _entries = [
            ["A", "2.4", "2.4", "0", "1"],
            ["A", "4.2", "2.4", "1", "0"],
            ["A", "4.2", "4.2", "0", "0"],
            ["A", "2.4", "4.2", "1", "1"],
        ]
        _builder = KoswatCsvFomBuilder()
        _builder.headers = _headers
        _builder.entries = _entries

        # 2. Run test.
        _koswat_fom = _builder.build()

        # 3. Verify expectations.
        assert isinstance(_koswat_fom, KoswatCsvFom)
        assert _koswat_fom.distances_list == [24, 42]
        assert len(_koswat_fom.points_surroundings_list) == len(_entries)
        assert _koswat_fom.is_valid()

        def check_point(
            point: PointSurroundings, location: Point, distances: List[float]
        ):
            assert isinstance(point, PointSurroundings)
            assert point.is_valid()
            assert point.section == "A"
            assert point.location.almost_equals(location, 0.001)
            assert point.distance_to_buildings == distances

        _points = _koswat_fom.points_surroundings_list
        check_point(_points[0], Point(2.4, 2.4), [42])
        check_point(_points[1], Point(4.2, 2.4), [24])
        check_point(_points[2], Point(4.2, 4.2), [])
        check_point(_points[3], Point(2.4, 4.2), [24, 42])
