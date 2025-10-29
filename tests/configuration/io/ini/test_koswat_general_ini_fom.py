from pathlib import Path
from configparser import ConfigParser
from koswat.configuration.io.ini.koswat_general_ini_fom import SurroundingsSectionFom
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class TestSurroundingsSectionFom:

    def test_initialize(self):
        _surroundings_section_fom = SurroundingsSectionFom(
            surroundings_database_dir=Path("/some/path"),
            construction_distance=100.0,
            construction_buffer=20.0,
            waterside=True,
            buildings=True,
            railways=True,
            waters=True,
            custom=True,
        )

        # 2. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatIniFomProtocol)
        assert _surroundings_section_fom.surroundings_database_dir == Path("/some/path")
        assert _surroundings_section_fom.construction_distance == 100.0
        assert _surroundings_section_fom.construction_buffer == 20.0
        assert _surroundings_section_fom.waterside is True
        assert _surroundings_section_fom.buildings is True
        assert _surroundings_section_fom.railways is True
        assert _surroundings_section_fom.waters is True
        assert _surroundings_section_fom.custom is True

    def test_from_config_without_omgevingtypes(self):
           # 1. Define test data.
        ini_config = ConfigParser()
        ini_config["SurroundingsSectionFom"] = {
            "omgevingsdatabases": "/some/path",
            "constructieafstand": 100.0,
            "constructieovergang": 20.0,
        }

        # 2. Run test.
        _surroundings_section_fom = SurroundingsSectionFom.from_config(ini_config["SurroundingsSectionFom"])

        # 3. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatIniFomProtocol)
        assert _surroundings_section_fom.surroundings_database_dir == Path("/some/path")
        assert _surroundings_section_fom.construction_distance == 100.0
        assert _surroundings_section_fom.construction_buffer == 20.0
        assert _surroundings_section_fom.waterside is False
        assert _surroundings_section_fom.buildings is False
        assert _surroundings_section_fom.railways is False
        assert _surroundings_section_fom.waters is False
        assert _surroundings_section_fom.custom is False

    def test_from_config_with_omgevingtypes(self):
        # 1. Define test data.
        ini_config = ConfigParser()
        ini_config["SurroundingsSectionFom"] = {
            "omgevingsdatabases": "/some/path",
            "constructieafstand": 100.0,
            "constructieovergang": 20.0,
            "omgevingtypes": "buitendijks,bebouwing,spoorwegen,water,custom"
        }

        # 2. Run test.
        _surroundings_section_fom = SurroundingsSectionFom.from_config(ini_config["SurroundingsSectionFom"])
        
        # 3. Verify expectations.
        assert isinstance(_surroundings_section_fom, KoswatIniFomProtocol)
        assert _surroundings_section_fom.surroundings_database_dir == Path("/some/path")
        assert _surroundings_section_fom.construction_distance == 100.0
        assert _surroundings_section_fom.construction_buffer == 20.0
        assert _surroundings_section_fom.waterside is True
        assert _surroundings_section_fom.buildings is True
        assert _surroundings_section_fom.railways is True
        assert _surroundings_section_fom.waters is True
        assert _surroundings_section_fom.custom is True