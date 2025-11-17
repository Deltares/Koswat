from typing import Type

import pytest

from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
)
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol
from koswat.core.io.ini.koswat_ini_reader import KoswatIniReader
from tests import test_data

test_ini_reader_data = test_data.joinpath("ini_reader")


class TestReadIniConfigurations:
    @pytest.mark.parametrize(
        "test_file, ini_fom_type",
        [
            pytest.param(
                "koswat_scenario.ini", KoswatSectionScenariosIniFom, id="Scenario INI"
            ),
        ],
    )
    def test_koswat_ini_reader_returns_fom_instance(
        self, test_file: str, ini_fom_type: Type[KoswatIniFomProtocol]
    ):
        # 1. Define test data.
        _test_file_path = test_ini_reader_data / test_file
        assert _test_file_path, "Test file not found at {}".format(_test_file_path)
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = ini_fom_type

        # 2. Run test.
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Verify expectations.
        assert isinstance(_ini_fom, ini_fom_type)
        assert isinstance(_ini_fom, FileObjectModelProtocol)

    def test_koswat_ini_read_scenario_ini(self):
        # 1. Define test data.
        _test_file_path = test_ini_reader_data / "koswat_scenario.ini"
        _ini_reader = KoswatIniReader()
        _ini_reader.koswat_ini_fom_type = KoswatSectionScenariosIniFom

        # 2. Run test
        _ini_fom = _ini_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_ini_fom, KoswatSectionScenariosIniFom)

        # Scenarios
        assert len(_ini_fom.section_scenarios) == 2

        # Scenario 0
        assert _ini_fom.section_scenarios[0].d_h == 0.5
        assert _ini_fom.section_scenarios[0].d_s == 10
        assert _ini_fom.section_scenarios[0].d_p == 50
        assert _ini_fom.section_scenarios[0].waterside_slope == None
        assert _ini_fom.section_scenarios[0].crest_width == None

        # Scenario 1
        assert _ini_fom.section_scenarios[1].d_h == 1
        assert _ini_fom.section_scenarios[1].d_s == 15
        assert _ini_fom.section_scenarios[1].d_p == 75
        assert _ini_fom.section_scenarios[1].waterside_slope == 4
        assert _ini_fom.section_scenarios[1].crest_width == 10
