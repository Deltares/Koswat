from pathlib import Path

from koswat.configuration.io.config_sections.surroundings_section_fom import (
    SurroundingsSectionFom,
)
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class TestSurroundingsSectionFom:

    def test_initialize(self):
        _surroundings_section_fom = SurroundingsSectionFom(
            construction_distance=100.0,
            construction_buffer=20.0,
            waterside=True,
            buildings=True,
            railways=True,
            waters=True,
        )

        # 2. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatIniFomProtocol)
        assert _surroundings_section_fom.construction_distance == 100.0
        assert _surroundings_section_fom.construction_buffer == 20.0
        assert _surroundings_section_fom.waterside is True
        assert _surroundings_section_fom.buildings is True
        assert _surroundings_section_fom.railways is True
        assert _surroundings_section_fom.waters is True
        assert _surroundings_section_fom.custom_obstacles == []

    def test_from_config_without_omgevingtypes(self):
        # 1. Define test data.
        _surroundings_config = {
            "constructieafstand": 100.0,
            "constructieovergang": 20.0,
        }

        # 2. Run test.
        _surroundings_section_fom = SurroundingsSectionFom.from_config(
            _surroundings_config
        )

        # 3. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatIniFomProtocol)
        assert _surroundings_section_fom.construction_distance == 100.0
        assert _surroundings_section_fom.construction_buffer == 20.0
        assert _surroundings_section_fom.waterside is False
        assert _surroundings_section_fom.buildings is False
        assert _surroundings_section_fom.railways is False
        assert _surroundings_section_fom.waters is False
        assert _surroundings_section_fom.custom_obstacles == []

    def test_from_config_with_omgevingtypes(self):
        # 1. Define test data.
        _surroundings_config = {
            "constructieafstand": 100.0,
            "constructieovergang": 20.0,
            "omgevingtypes": [
                "buitendijks",
                "bebouwing",
                "spoorwegen",
                "water",
                "camping",
                "wildlife",
            ],
        }

        # 2. Run test.
        _surroundings_section_fom = SurroundingsSectionFom.from_config(
            _surroundings_config
        )

        # 3. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatIniFomProtocol)
        assert _surroundings_section_fom.construction_distance == 100.0
        assert _surroundings_section_fom.construction_buffer == 20.0
        assert _surroundings_section_fom.waterside is True
        assert _surroundings_section_fom.buildings is True
        assert _surroundings_section_fom.railways is True
        assert _surroundings_section_fom.waters is True
        assert _surroundings_section_fom.custom_obstacles == ["camping", "wildlife"]
