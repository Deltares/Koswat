from pathlib import Path

from koswat.configuration.io.ini.koswat_scenario_list_ini_dir_reader import (
    KoswatSectionScenarioListIniDirReader,
)
from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
)
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from tests import test_data


class TestKoswatScenarioListIniDirReader:
    def test_initialize(self):
        _reader = KoswatSectionScenarioListIniDirReader()
        assert isinstance(_reader, KoswatSectionScenarioListIniDirReader)
        assert isinstance(_reader, KoswatReaderProtocol)
        assert _reader.dike_selection == []

    def test_selected_scenario_not_selected_scenario(self):
        # 1. Define test data
        _reader = KoswatSectionScenarioListIniDirReader()
        _reader.dike_selection = []
        _test_file = test_data / "acceptance" / "scenarios" / "10-1-1-A-1-A.ini"
        assert _test_file.exists()

        # 2. Run test.
        _selected = _reader._selected_scenario(_test_file)

        # 3. Verify expectations.
        # All will be selected.
        assert _selected == True

    def test_selected_scenario_selected_scenario(self):
        # 1. Define test data
        _reader = KoswatSectionScenarioListIniDirReader()
        _reader.dike_selection = ["dumb_scenario"]
        _test_file = test_data / "acceptance" / "scenarios" / "10-1-1-A-1-A.ini"
        assert _test_file.exists()

        # 2. Run test.
        _selected = _reader._selected_scenario(_test_file)

        # 3. Verify expectations.
        assert _selected == False

    def test_get_scenario(self):
        # 1. Define test data
        _reader = KoswatSectionScenarioListIniDirReader()
        _test_file = test_data / "acceptance" / "scenarios" / "10-1-1-A-1-A.ini"
        assert _test_file.exists()

        # 2. Run test.
        _scenario_fom = _reader._get_scenario(_test_file)

        # 3. Verify expectations.
        assert isinstance(_scenario_fom, KoswatSectionScenariosIniFom)
        assert _scenario_fom.scenario_section == _test_file.stem

    def test_read_without_dir(self):
        _result = KoswatSectionScenarioListIniDirReader().read(Path("not_a_dir"))
        assert _result == []

    def test_read(self):
        # 1. Define test data
        _reader = KoswatSectionScenarioListIniDirReader()
        _test_dir = test_data / "acceptance" / "scenarios"
        assert _test_dir.exists()

        # 2. Run test.
        _list_fom = _reader.read(_test_dir)

        # 3. Verify expectations.
        assert any(_list_fom)
        assert all(isinstance(_fom, KoswatSectionScenariosIniFom) for _fom in _list_fom)
