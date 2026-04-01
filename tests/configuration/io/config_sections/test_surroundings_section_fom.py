import math
import pytest

from koswat.configuration.io.config_sections.surroundings_section_fom import (
    SurroundingsSectionFom,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


class TestSurroundingsSectionFom:

    def test_initialize(self):
        _surroundings_section_fom = SurroundingsSectionFom(
            construction_distance=100.0,
            construction_buffer=20.0,
            allow_waterside_reinforcement=True,
            obstacle_types={"bebouwing": 5, "spoorwegen": 10, "water": None},
        )

        # 2. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatJsonFomProtocol)
        assert _surroundings_section_fom.construction_distance == 100.0
        assert _surroundings_section_fom.construction_buffer == 20.0
        assert _surroundings_section_fom.allow_waterside_reinforcement is True
        assert _surroundings_section_fom.obstacle_types == {
            "bebouwing": 5,
            "spoorwegen": 10,
            "water": None,
        }

    def test_when_from_config_given_set_defaults_false_then_expected_values_set(self):
        # 1. Define test data.
        _surroundings_config = {
        }

        # 2. Run test.
        _surroundings_section_fom = SurroundingsSectionFom.from_config(
            _surroundings_config, set_defaults=False
        )

        # 3. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatJsonFomProtocol)
        assert _surroundings_section_fom.construction_distance == None
        assert _surroundings_section_fom.construction_buffer == None
        assert _surroundings_section_fom.allow_waterside_reinforcement == None
        assert _surroundings_section_fom.obstacle_types == {}

    def test_when_from_config_given_set_defaults_true_then_expected_values_set(self):
        # 1. Define test data.
        _surroundings_config = {
        }

        # 2. Run test.
        _surroundings_section_fom = SurroundingsSectionFom.from_config(
            _surroundings_config, set_defaults=True
        )

        # 3. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatJsonFomProtocol)
        assert math.isnan(_surroundings_section_fom.construction_distance)
        assert math.isnan(_surroundings_section_fom.construction_buffer)
        assert _surroundings_section_fom.allow_waterside_reinforcement is True
        assert _surroundings_section_fom.obstacle_types == {}

    def test_from_config_with_omgevingtypes(self):
        # 1. Define test data.
        _surroundings_config = {
            "constructieafstand": 100.0,
            "constructieovergang": 20.0,
            "buitendijks": True,
            "omgevingtypes": [
                {"type": "bebouwing", "buffer": 5},
                {"type": "spoorwegen", "buffer": 10},
                {"type": "water"},
            ],
            "toegestaanbuitenzijdeversterking": False
        }

        # 2. Run test.
        _surroundings_section_fom = SurroundingsSectionFom.from_config(
            _surroundings_config, set_defaults=False
        )

        # 3. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatJsonFomProtocol)
        assert _surroundings_section_fom.construction_distance == 100.0
        assert _surroundings_section_fom.construction_buffer == 20.0
        assert _surroundings_section_fom.allow_waterside_reinforcement is False
        assert _surroundings_section_fom.obstacle_types == {
            "bebouwing": 5,
            "spoorwegen": 10,
            "water": None,
        }

    def test_from_config_with_invalid_buffer(self):
        # 1. Define test data.
        _surroundings_config = {
            "constructieafstand": 100.0,
            "constructieovergang": 20.0,
            "buitendijks": True,
            "omgevingtypes": [{"type": "bebouwing", "buffer": "invalid_buffer"}],
        }

        # 2. Run test
        with pytest.raises(ValueError) as exc_info:
            SurroundingsSectionFom.from_config(_surroundings_config, set_defaults=True)

        # 3. Verify expectations.
        assert exc_info is not None
