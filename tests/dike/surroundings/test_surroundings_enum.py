import pytest

from koswat.dike.surroundings.road_class import RoadsClass
from koswat.dike.surroundings.surroundings_enum import SurroundingsEnum
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle


class TestSurroundingsEnum:

    @pytest.mark.parametrize(
        "input_str, expected_enum, expected_surrounding_type, expected_name",
        [
            pytest.param(
                "wegen_binnendijks_klasse2",
                SurroundingsEnum.ROADS_CLASS_2_POLDERSIDE,
                SurroundingsInfrastructure,
                "roads_class_2_polderside",
            ),
            pytest.param(
                "wegen_binnendijks_klasse7",
                SurroundingsEnum.ROADS_CLASS_7_POLDERSIDE,
                SurroundingsInfrastructure,
                "roads_class_7_polderside",
            ),
            pytest.param(
                "wegen_binnendijks_klasse24",
                SurroundingsEnum.ROADS_CLASS_24_POLDERSIDE,
                SurroundingsInfrastructure,
                "roads_class_24_polderside",
            ),
            pytest.param(
                "wegen_binnendijks_klasse47",
                SurroundingsEnum.ROADS_CLASS_47_POLDERSIDE,
                SurroundingsInfrastructure,
                "roads_class_47_polderside",
            ),
            pytest.param(
                "wegen_binnendijks_klasseonbekend",
                SurroundingsEnum.ROADS_CLASS_UNKNOWN_POLDERSIDE,
                SurroundingsInfrastructure,
                "roads_class_unknown_polderside",
            ),
            pytest.param(
                "wegen_buitendijks_klasse2",
                SurroundingsEnum.ROADS_CLASS_2_WATERSIDE,
                SurroundingsInfrastructure,
                "roads_class_2_waterside",
            ),
            pytest.param(
                "wegen_buitendijks_klasse7",
                SurroundingsEnum.ROADS_CLASS_7_WATERSIDE,
                SurroundingsInfrastructure,
                "roads_class_7_waterside",
            ),
            pytest.param(
                "wegen_buitendijks_klasse24",
                SurroundingsEnum.ROADS_CLASS_24_WATERSIDE,
                SurroundingsInfrastructure,
                "roads_class_24_waterside",
            ),
            pytest.param(
                "wegen_buitendijks_klasse47",
                SurroundingsEnum.ROADS_CLASS_47_WATERSIDE,
                SurroundingsInfrastructure,
                "roads_class_47_waterside",
            ),
            pytest.param(
                "wegen_buitendijks_klasseonbekend",
                SurroundingsEnum.ROADS_CLASS_UNKNOWN_WATERSIDE,
                SurroundingsInfrastructure,
                "roads_class_unknown_waterside",
            ),
        ],
    )
    def test_translate_known_types(
        self,
        input_str: str,
        expected_enum: SurroundingsEnum,
        expected_surrounding_type: type[
            SurroundingsInfrastructure | SurroundingsObstacle
        ],
        expected_name: str,
    ):
        # 1. Run test.
        _result = SurroundingsEnum.translate(input_str)

        # 2. Verify results.
        assert _result == expected_enum
        assert _result.surrounding_type == expected_surrounding_type
        assert _result.dutch_text == input_str
        assert _result.name.lower() == expected_name

    def test_translate_unknown_type_returns_obstacle(self):
        # 1. Define test data.
        _expected_enum = SurroundingsEnum.OBSTACLE

        # 2. Run test.
        _result = SurroundingsEnum.translate("unknown_type")

        # 3. Verify results.
        assert _result == _expected_enum

    @pytest.mark.parametrize(
        "road_class", [pytest.param(_rc, id=f"Road class: {_rc}") for _rc in RoadsClass]
    )
    def test_when_get_infra_types_given_road_class_returns_infra_types(
        self, road_class: RoadsClass
    ):
        # 1. Run test.
        _result = SurroundingsEnum.get_infra_types(road_class)

        # 2. Verify results.
        assert isinstance(_result, tuple)
        assert len(_result) == 2
        assert all(isinstance(item, SurroundingsEnum) for item in _result)
        assert all(
            item.surrounding_type == SurroundingsInfrastructure for item in _result
        )
        assert all(road_class.name.lower() in item.name.lower() for item in _result)

    def test_when_get_infra_types_given_invalid_road_class_returns_nones(self):
        # 1. Define test data.
        _invalid_road_class = "invalid_road_class"

        # 2. Run test.
        _result = SurroundingsEnum.get_infra_types(_invalid_road_class)

        # 3. Verify results.
        assert _result == (None, None)
