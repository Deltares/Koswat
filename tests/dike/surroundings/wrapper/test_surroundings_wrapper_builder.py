from typing import List

import pytest
from shapely.geometry import Point

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.configuration.io.shp import KoswatDikeLocationsShpFom
from koswat.core.protocols import BuilderProtocol
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside_builder import (
    KoswatBuildingsPoldersideBuilder,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike.surroundings.wrapper.surroundings_wrapper_builder import (
    SurroundingsWrapperBuilder,
)
from tests import test_data


class TestSurroundingsWrapperBuilder:
    def test_initialize_builder(self):
        _builder = SurroundingsWrapperBuilder()
        assert isinstance(_builder, SurroundingsWrapperBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.trajects_fom
        assert not _builder.surroundings_fom

    def _as_surrounding_point(
        self, location: Point, distances: List[float]
    ) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = location
        _ps.distance_to_surroundings = distances
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

        # Traject wrapper
        _koswat_shp_fom = KoswatDikeLocationsShpFom()
        _koswat_shp_fom.initial_point = _start_point
        _koswat_shp_fom.end_point = _end_point

        # 2. Run test.
        with pytest.raises(ValueError) as _err_info:
            _builder = SurroundingsWrapperBuilder()
            _builder.trajects_fom = _koswat_shp_fom
            _builder.surroundings_fom = _surroundings_wrapper
            _surroundings = _builder.build()
