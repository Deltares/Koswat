from collections.abc import Callable

import pytest

from koswat.dike.surroundings.point import (
    PointInfrastructureSurroundings,
    PointObstacleSurroundings,
    PointSurroundingsProtocol,
)
from tests.conftest import PointSurroundingsTestCase


class TestPointInfrastructureSurroundings:
    def test_initialize_point_surroundings(self):
        _p_s = PointInfrastructureSurroundings()
        assert isinstance(_p_s, PointInfrastructureSurroundings)
        assert isinstance(_p_s, PointSurroundingsProtocol)
        assert not _p_s.section
        assert not _p_s.location
        assert not _p_s.polderside_surroundings

    def test_when_merge_given_valid_input_then_merges_correctly(self):
        # 1. Define test data.
        _polderside_surroundings = {10: 1.0, 20: 2.0}
        _waterside_surroundings = {50: 5.0, 60: 6.0}
        _polderside = PointInfrastructureSurroundings(
            imported_surroundings=_polderside_surroundings
        )
        _waterside = PointInfrastructureSurroundings(
            imported_surroundings=_waterside_surroundings
        )

        # 2. Run test.
        _polderside.merge(_waterside)

        # 3. Verify expectations.
        assert _polderside.polderside_surroundings == _polderside_surroundings
        assert _polderside.waterside_surroundings == _waterside_surroundings

    def test_when_merge_given_invalid_input_then_raises_type_error(self):
        _polderside = PointInfrastructureSurroundings()
        _waterside = PointObstacleSurroundings()
        with pytest.raises(TypeError):
            _polderside.merge(_waterside)

    def test_get_total_infrastructure_per_zone_with_costs_calculator_case(
        self,
        point_surroundings_for_zones_builder_fixture: tuple[
            Callable[[], PointInfrastructureSurroundings], PointSurroundingsTestCase
        ],
    ):
        # 1. Define test data.
        (
            _point_surroundings_builder,
            _point_surroundings_case,
        ) = point_surroundings_for_zones_builder_fixture
        _ps = _point_surroundings_builder()
        assert isinstance(_ps, PointInfrastructureSurroundings)
        assert isinstance(_ps, PointSurroundingsProtocol)

        # 2. Run test.
        _result = _ps.get_total_infrastructure_per_zone(
            _point_surroundings_case.zone_a_limits,
            _point_surroundings_case.zone_b_limits,
            _point_surroundings_case.zone_c_limits,
        )

        # 3. Verify expectations.
        assert _result == _point_surroundings_case.expected_total_lengths

    @pytest.mark.parametrize(
        "zones, polderside_surroundings, expected_values",
        [
            pytest.param(
                [(-5, 0), (0, 5), (5, 25)],
                {30: 0, 35: 5},
                [0.0, 0.0, 0.0],
                id="No infra in zone A, B or C.",
            ),
            pytest.param(
                [(-5, 0), (0, 8), (8, 76)],
                {5.0: 0.0, 10.0: 1.0, 20.0: 0.0, 25.0: 1.0},
                [0.0, 1.0, 1.0],
                id="Overlapping distances.",
            ),
        ],
    )
    def test_get_total_infrastructure_per_zone_given_zones_and_surround_matrix(
        self,
        zones: list[tuple[float, float]],
        polderside_surroundings: dict[float, float],
        expected_values: list[float],
    ):
        # 1. Define test data.
        _ps = PointInfrastructureSurroundings(
            polderside_surroundings=polderside_surroundings
        )

        # 2. Run test.
        _total_infra = _ps.get_total_infrastructure_per_zone(*zones)

        # 3. Verify expectations.
        assert _total_infra == expected_values
