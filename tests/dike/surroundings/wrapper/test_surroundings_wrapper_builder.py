from shapely.geometry import Point

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.configuration.io.shp import KoswatDikeLocationsShpFom
from koswat.core.protocols import BuilderProtocol
from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside import (
    PointSurroundings,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper_builder import (
    SurroundingsWrapperBuilder,
)


class TestSurroundingsWrapperBuilder:
    def test_initialize_builder(self):
        # 1. Define test data.
        _surroundings_fom = None
        _surroundings_section = None
        _trajects_fom = None

        # 2. Run test.
        _builder = SurroundingsWrapperBuilder(
            surroundings_section=_surroundings_section,
            surroundings_fom=_surroundings_fom,
            trajects_fom=_trajects_fom,
        )

        # 3. Verify expectations
        assert isinstance(_builder, SurroundingsWrapperBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert _builder.trajects_fom == _trajects_fom
        assert _builder.surroundings_fom == _surroundings_fom
        assert _builder.surroundings_section == _surroundings_section

    def _as_surrounding_point(
        self, location: Point, distances: list[float]
    ) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = location
        _ps.distance_to_surroundings_dict = distances
        return _ps

    def test_given_valid_data_build_returns_surroundings(self):
        # 1. Define test data.
        _end_point = Point(4.2, 4.2)
        _start_point = Point(4.2, 2.4)
        _expected_points = [
            _start_point,
            Point(2.4, 4.2),
            _end_point,
        ]

        # Surroundings wrapper
        _surroundings_csv_fom = KoswatTrajectSurroundingsCsvFom()
        _surroundings_csv_fom.points_surroundings_list = [
            self._as_surrounding_point(Point(2.4, 2.4), [2.4]),
            self._as_surrounding_point(_start_point, [2.4]),
            self._as_surrounding_point(Point(2.4, 4.2), [2.4]),
            self._as_surrounding_point(_end_point, [2.4]),
        ]
        _surroundings_wrapper = KoswatTrajectSurroundingsWrapperCsvFom()
        _surroundings_wrapper.buildings_polderside = _surroundings_csv_fom

        _surroundings_section = SurroundingsSectionFom(
            surroundings_database_dir=None,
            buitendijks=False,
            bebouwing=True,
            spoorwegen=False,
            water=False,
            constructieafstand=4.2,
            constructieovergang=2.4,
        )

        # Traject wrapper
        _koswat_shp_fom = KoswatDikeLocationsShpFom()
        _koswat_shp_fom.initial_point = _start_point
        _koswat_shp_fom.end_point = _end_point

        # 2. Run test.
        _surroundings = SurroundingsWrapperBuilder(
            trajects_fom=_koswat_shp_fom,
            surroundings_fom=_surroundings_wrapper,
            surroundings_section=_surroundings_section,
        ).build()

        assert [
            _point.location for _point in _surroundings.buildings_polderside.points
        ] == _expected_points
