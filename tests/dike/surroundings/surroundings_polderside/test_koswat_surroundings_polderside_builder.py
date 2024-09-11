from typing import Iterator

import pytest
from shapely.geometry import Point

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_reader import (
    KoswatSurroundingsCsvReader,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_reader import (
    KoswatDikeLocationsListShpReader,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.koswat_point_surroundings_polderside_builder import (
    KoswatPointSurroundingsPoldersideBuilder,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from tests import test_data


class TestKoswatSurroundingsPoldersideBuilder:
    def test_initialize_builder(self):
        _builder = KoswatPointSurroundingsPoldersideBuilder(None, None)
        assert isinstance(_builder, KoswatPointSurroundingsPoldersideBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.koswat_shp_fom
        assert not _builder.koswat_csv_fom

    def _as_surrounding_point(
        self, location: Point, distances: list[float]
    ) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = location
        _ps.distance_to_surroundings = distances
        return _ps

    def test_find_conflicting_point_idx_raises_error_if_not_found(self):
        # 1. Define test data.
        _builder = KoswatPointSurroundingsPoldersideBuilder(
            koswat_csv_fom=KoswatTrajectSurroundingsCsvFom(), koswat_shp_fom=None
        )

        # 2. Run test
        with pytest.raises(ValueError) as exc_err:
            _builder._find_polderside_point_idx(None)

        # 3. Verify expectations.
        assert (
            str(exc_err.value)
            == "No point fromt the *.shp file matches the ones in the *.csv file."
        )

    @pytest.fixture(name="valid_builder")
    def _get_valid_koswat_point_surroundings_polderside_builder(
        self,
    ) -> Iterator[KoswatPointSurroundingsPoldersideBuilder]:
        _koswat_csv_fom = KoswatTrajectSurroundingsCsvFom()
        _koswat_csv_fom.points_surroundings_list = [
            self._as_surrounding_point(Point(2.4, 2.4), []),
            self._as_surrounding_point(Point(4.2, 2.4), []),
            self._as_surrounding_point(Point(2.4, 4.2), []),
            self._as_surrounding_point(Point(4.2, 4.2), []),
        ]
        yield KoswatPointSurroundingsPoldersideBuilder(
            koswat_csv_fom=_koswat_csv_fom, koswat_shp_fom=None
        )

    @pytest.mark.parametrize(
        "limit_point",
        [
            pytest.param(Point(2.4, 4.2), id="Basic point"),
            pytest.param(Point(2.401, 4.201), id="With some decimals"),
        ],
    )
    def test_find_conflicting_point_idx_returns_value(
        self,
        limit_point: Point,
        valid_builder: KoswatPointSurroundingsPoldersideBuilder,
    ):
        # 1. Define test data.
        assert isinstance(valid_builder, KoswatPointSurroundingsPoldersideBuilder)

        # 2. Run test.
        _idx_found = valid_builder._find_polderside_point_idx(limit_point)

        # 3. Verify expectations.
        assert _idx_found == 2

    @pytest.mark.parametrize(
        "start_idx, end_idx",
        [
            pytest.param(1, 3, id="Normal ordering"),
            pytest.param(3, 1, id="Reverse ordering"),
        ],
    )
    def test_get_conflicting_points_regardless_of_index_order(
        self,
        start_idx: int,
        end_idx: int,
        valid_builder: KoswatPointSurroundingsPoldersideBuilder,
    ):
        assert isinstance(valid_builder, KoswatPointSurroundingsPoldersideBuilder)
        _expected_points = [
            Point(4.2, 2.4),
            Point(2.4, 4.2),
            Point(4.2, 4.2),
        ]

        # 2. Run test.
        _found_points = valid_builder._get_polderside_points(start_idx, end_idx)

        # 3. Verify expectations.
        assert _found_points == _expected_points

    def test_build_given_valid_data_then_returns_koswat_building_polderside(self):
        # 1. Define test data
        _end_point = Point(4.2, 4.2)
        _start_point = Point(4.2, 2.4)
        _expected_points = [
            _start_point,
            Point(2.4, 4.2),
            _end_point,
        ]
        _koswat_csv_fom = KoswatTrajectSurroundingsCsvFom()
        _koswat_csv_fom.points_surroundings_list = [
            self._as_surrounding_point(Point(2.4, 2.4), [2.4]),
            self._as_surrounding_point(_start_point, [2.4]),
            self._as_surrounding_point(Point(2.4, 4.2), [2.4]),
            self._as_surrounding_point(_end_point, [2.4]),
        ]
        assert _koswat_csv_fom.is_valid()
        _koswat_shp_fom = KoswatDikeLocationsShpFom()
        _koswat_shp_fom.end_point = _end_point
        _koswat_shp_fom.initial_point = _start_point
        assert _koswat_shp_fom.is_valid()

        # 2. Run test.
        _kbp = KoswatPointSurroundingsPoldersideBuilder(
            koswat_csv_fom=_koswat_csv_fom, koswat_shp_fom=_koswat_shp_fom
        ).build()

        # 3. Verify expectations.
        assert isinstance(_kbp, KoswatSurroundingsProtocol)
        assert len(_kbp.conflicting_points) == len(_expected_points)

    def test_from_files_then_build_returns_expected_model(self):
        # 1. Define test data.
        _csv_test_file = test_data.joinpath(
            "csv_reader", "Omgeving", "T_10_3_bebouwing_binnendijks.csv"
        )
        _shp_test_file = test_data.joinpath(
            "shp_reader",
            "Dijkvak",
            "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp",
        )
        assert _csv_test_file.is_file()
        assert _shp_test_file.is_file()

        _shp_fom_builder = KoswatDikeLocationsListShpReader()
        _shp_fom_builder.selected_locations = []
        _koswat_wrapper_shp_fom = _shp_fom_builder.read(_shp_test_file)

        # 2. Run test
        _buildings = KoswatPointSurroundingsPoldersideBuilder(
            koswat_csv_fom=KoswatSurroundingsCsvReader().read(_csv_test_file),
            koswat_shp_fom=_koswat_wrapper_shp_fom[0],
        ).build()

        # 3. Verify expectations.
        assert isinstance(_buildings, KoswatSurroundingsProtocol)
        assert len(_buildings.points) == 3728
        assert _buildings.conflicting_points
