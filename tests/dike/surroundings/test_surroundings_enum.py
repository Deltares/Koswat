import pytest

from koswat.dike.surroundings.surroundings_enum import SurroundingsEnum
from koswat.dike.surroundings.surroundings_infrastructure import SurroundingsInfrastructure
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle

class TestSurroundingsEnum:

    @pytest.mark.parametrize("input_str, expected_enum, expected_surrounding_type, expected_name", 
                             [ 
                                pytest.param("bebouwing", SurroundingsEnum.BUILDINGS, SurroundingsObstacle, "buildings"),
                                pytest.param("spoorwegen", SurroundingsEnum.RAILWAYS, SurroundingsObstacle, "railways"),
                                pytest.param("water", SurroundingsEnum.WATERS, SurroundingsObstacle, "waters"),
                                pytest.param("wegen_binnendijks_klasse2", SurroundingsEnum.ROADS_CLASS_2_POLDERSIDE, SurroundingsInfrastructure, "roads_class_2_polderside"),
                                pytest.param("wegen_binnendijks_klasse7", SurroundingsEnum.ROADS_CLASS_7_POLDERSIDE, SurroundingsInfrastructure, "roads_class_7_polderside"),
                                pytest.param("wegen_binnendijks_klasse24", SurroundingsEnum.ROADS_CLASS_24_POLDERSIDE, SurroundingsInfrastructure, "roads_class_24_polderside"),
                                pytest.param("wegen_binnendijks_klasse47", SurroundingsEnum.ROADS_CLASS_47_POLDERSIDE, SurroundingsInfrastructure, "roads_class_47_polderside"),
                                pytest.param("wegen_binnendijks_klasseonbekend", SurroundingsEnum.ROADS_CLASS_UNKNOWN_POLDERSIDE, SurroundingsInfrastructure, "roads_class_unknown_polderside"),
                                pytest.param("wegen_buitendijks_klasse2", SurroundingsEnum.ROADS_CLASS_2_WATERSIDE, SurroundingsInfrastructure, "roads_class_2_waterside"),
                                pytest.param("wegen_buitendijks_klasse7", SurroundingsEnum.ROADS_CLASS_7_WATERSIDE, SurroundingsInfrastructure, "roads_class_7_waterside"),
                                pytest.param("wegen_buitendijks_klasse24", SurroundingsEnum.ROADS_CLASS_24_WATERSIDE, SurroundingsInfrastructure, "roads_class_24_waterside"),
                                pytest.param("wegen_buitendijks_klasse47", SurroundingsEnum.ROADS_CLASS_47_WATERSIDE, SurroundingsInfrastructure, "roads_class_47_waterside"),
                                pytest.param("wegen_buitendijks_klasseonbekend", SurroundingsEnum.ROADS_CLASS_UNKNOWN_WATERSIDE, SurroundingsInfrastructure, "roads_class_unknown_waterside"),
                             ])
    def test_translate_known_types(self, input_str: str, expected_enum: SurroundingsEnum, expected_surrounding_type: type[SurroundingsInfrastructure | SurroundingsObstacle], expected_name: str):
        # 1. Run test.
        _result = SurroundingsEnum.translate(input_str)

        # 2. Verify results.
        assert _result == expected_enum
        assert _result.surrounding_type == expected_surrounding_type
        assert _result.dutch_text == input_str
        assert _result.name.lower() == expected_name

    def test_translate_unknown_type_raises_value_error(self):
        # 1. Define test data.
        _expected_error = "No mapping found for unknown_type"

        # 2. Run test.
        with pytest.raises(ValueError) as exc_info:
            SurroundingsEnum.translate("unknown_type")
        
        # 3. Verify results.
        assert str(exc_info.value) == _expected_error