from typing import List

import pytest
from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.io.csv import KoswatCsvFom, KoswatCsvFomBuilder
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class TestKoswatCsvFom:
    def test_initialize_koswat_csv_fom(self):
        _csv_fom = KoswatCsvFom()
        assert isinstance(_csv_fom, KoswatCsvFom)
        assert isinstance(_csv_fom, FileObjectModelProtocol)
        assert not _csv_fom.points_surroundings_list
        assert not _csv_fom.is_valid()


class TestKoswatCsvFomBuilder:
    def _check_point(
        self, point: PointSurroundings, location: Point, distances: List[float]
    ):
        assert isinstance(point, PointSurroundings)
        assert point.section == "A"
        assert point.location.is_valid
        assert point.location.almost_equals(location, 0.001)
        assert point.distance_to_buildings == distances

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

        _points = _koswat_fom.points_surroundings_list
        self._check_point(_points[0], Point(2.4, 2.4), [42])
        self._check_point(_points[1], Point(4.2, 2.4), [24])
        self._check_point(_points[2], Point(4.2, 4.2), [])
        self._check_point(_points[3], Point(2.4, 4.2), [24, 42])

    def test_is_valid_fails_when_header_differs_with_entries(self):
        _builder = KoswatCsvFomBuilder()
        _builder.headers = ["a", "b"]
        _builder.entries = [["one"], ["two"], ["three"]]
        assert not _builder._is_valid()

    def test_raises_when_not_valid(self):
        _builder = KoswatCsvFomBuilder()
        assert not _builder._is_valid()
        with pytest.raises(ValueError) as exc_err:
            _builder.build()
        assert str(exc_err.value) == "Not valid headers and entries combination."

    @pytest.mark.parametrize(
        "distance_str",
        [
            pytest.param("afst45m45", id="Number duplicated"),
            pytest.param("afstm", id="No number provided"),
        ],
    )
    def test_get_surroundings_distances_raises_when_wrong_header(
        self, distance_str: str
    ):
        # 1. Define test data
        _builder = KoswatCsvFomBuilder()
        _expected_err = "More than one distance captured, distance headers should be like `afst_42m`."
        _distance_list = [distance_str]

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _builder._get_surroundings_distances(_distance_list)

        # 3. Verify expectations.
        assert str(exc_err.value) == _expected_err

    def test_get_surroundings_distances_returns_mapped_values(self):
        # 1. Define test data
        _builder = KoswatCsvFomBuilder()
        _distance_list = [f"afst_24m", f"afst_42m"]

        # 2. Run test.
        _distances = _builder._get_surroundings_distances(_distance_list)

        # 3. Verify expectations.
        assert _distances == [24, 42]

    def test_build_point_surroundings_returns_point(self):
        # 1. Define test data
        _builder = KoswatCsvFomBuilder()
        _distance_list = [24, 42]
        _entry = [0, "A", "2.4", "2.4", "0", "1"]

        # 2. Run test.
        _point_surroundings = _builder._build_point_surroundings(_entry, _distance_list)

        # 3. Verify expectations.
        assert isinstance(_point_surroundings, PointSurroundings)
        assert _point_surroundings.section == "A"
        assert _point_surroundings.location.x == 2.4
        assert _point_surroundings.location.y == 2.4
        assert _point_surroundings.distance_to_buildings == [42]

    def test_build_points_surroundings_list(self):
        # 1. Define test data
        _builder = KoswatCsvFomBuilder()
        _distance_list = [24, 42]
        _builder.entries = [
            ["A", "2.4", "2.4", "0", "1"],
            ["A", "4.2", "2.4", "1", "1"],
        ]

        # 2. Run test.
        _ps_list = _builder._build_points_surroundings_list(_distance_list)

        # 3. Verify expectations.
        assert isinstance(_ps_list, list)
        assert all(isinstance(_ps, PointSurroundings) for _ps in _ps_list)
        self._check_point(_ps_list[0], Point(2.4, 2.4), [42])
        self._check_point(_ps_list[1], Point(4.2, 2.4), [24, 42])
