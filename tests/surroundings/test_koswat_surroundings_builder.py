from typing import List

from shapely.geometry import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.io.koswat_csv_fom import KoswatCsvFom
from koswat.io.koswat_shp_reader import KoswatShpFom
from koswat.surroundings.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)
from koswat.surroundings.koswat_buildings_polderside_builder import (
    KoswatBuildingsPoldersideBuilder,
)
from koswat.surroundings.koswat_surroundings import KoswatSurroundings
from koswat.surroundings.koswat_surroundings_builder import KoswatSurroundingsBuilder
from tests import test_data


class TestKoswatSurroundingsBuilder:
    def test_initialize_builder(self):
        _builder = KoswatSurroundingsBuilder()
        assert isinstance(_builder, KoswatSurroundingsBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.buildings_foms

    def test_initialize_with_files(self):
        # 1. Define test data.
        _csv_test_file = (
            test_data / "csv_reader" / "Omgeving" / "T_10_3_bebouwing_binnendijks.csv"
        )
        _shp_test_file = (
            test_data
            / "shp_reader"
            / "Dijkvak"
            / "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp"
        )
        assert _csv_test_file.is_file()
        assert _shp_test_file.is_file()

        # 2. Run test
        _builder = KoswatSurroundingsBuilder.from_files(
            dict(csv_file=_csv_test_file, shp_file=_shp_test_file)
        )

        # 3. Verify expectations.
        assert isinstance(_builder, KoswatSurroundingsBuilder)
        assert isinstance(_builder.buildings_foms, KoswatBuildingsPoldersideBuilder)

    def _as_surrounding_point(
        self, location: Point, distances: List[float]
    ) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = location
        _ps.distance_to_buildings = distances
        return _ps

    def test_given_valid_data_build_returns_surroundings(self):
        # 1. Define test data.
        _buildings_foms = KoswatBuildingsPoldersideBuilder()
        _end_point = Point(4.2, 4.2)
        _start_point = Point(4.2, 2.4)
        _expected_points = [
            _start_point,
            Point(2.4, 4.2),
            _end_point,
        ]
        _buildings_foms.koswat_csv_fom = KoswatCsvFom()
        _buildings_foms.koswat_csv_fom.points_surroundings_list = [
            self._as_surrounding_point(Point(2.4, 2.4), [2.4]),
            self._as_surrounding_point(_start_point, [2.4]),
            self._as_surrounding_point(Point(2.4, 4.2), [2.4]),
            self._as_surrounding_point(_end_point, [2.4]),
        ]
        _buildings_foms.koswat_shp_fom = KoswatShpFom()
        _buildings_foms.koswat_shp_fom.end_point = _end_point
        _buildings_foms.koswat_shp_fom.initial_point = _start_point
        assert _buildings_foms.koswat_csv_fom.is_valid()
        assert _buildings_foms.koswat_shp_fom.is_valid()

        # 2. Run test.
        _builder = KoswatSurroundingsBuilder()
        _builder.buildings_foms = _buildings_foms
        _surroundings = _builder.build()
        # 3. Verify expectations.
        assert isinstance(_surroundings, KoswatSurroundings)
        assert isinstance(_surroundings.buldings_polderside, KoswatBuildingsPolderside)
        assert _surroundings.locations == _expected_points