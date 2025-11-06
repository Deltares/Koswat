from pathlib import Path

from koswat.configuration.io.json.koswat_scenario_list_json_dir_reader import (
    KoswatSectionScenarioListJsonDirReader,
)
from koswat.configuration.io.json.koswat_section_scenario_json_fom import (
    KoswatSectionScenariosJsonFom,
)
from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from tests import test_data


class TestKoswatScenarioListJsonDirReader:
    def test_initialize(self):
        _reader = KoswatSectionScenarioListJsonDirReader()
        assert isinstance(_reader, KoswatSectionScenarioListJsonDirReader)
        assert isinstance(_reader, KoswatReaderProtocol)
        assert _reader.dike_selection == []

    def test__selected_scenario_empty_selection(self):
        # 1. Define test data
        _reader = KoswatSectionScenarioListJsonDirReader(dike_selection=[])
        _test_file = test_data.joinpath("acceptance", "scenarios", "10-1-1-A-1-A.json")
        assert _test_file.exists()

        # 2. Run test.
        _selected = _reader._selected_scenario(_test_file)

        # 3. Verify expectations.
        assert _selected == False

    def test__selected_scenario_other_selection(self):
        # 1. Define test data
        _reader = KoswatSectionScenarioListJsonDirReader(
            dike_selection=["dumb_scenario"]
        )
        _test_file = test_data.joinpath("acceptance", "scenarios", "10-1-1-A-1-A.json")
        assert _test_file.exists()

        # 2. Run test.
        _selected = _reader._selected_scenario(_test_file)

        # 3. Verify expectations.
        assert _selected == False

    def test__selected_scenario_valid_selection(self):
        # 1. Define test data
        _reader = KoswatSectionScenarioListJsonDirReader(
            dike_selection=["10-1-1-A-1-A"]
        )
        _test_file = test_data.joinpath("acceptance", "scenarios", "10-1-1-A-1-A.json")
        assert _test_file.exists()

        # 2. Run test.
        _selected = _reader._selected_scenario(_test_file)

        # 3. Verify expectations.
        assert _selected == True

    def test__get_scenario(self):
        # 1. Define test data
        _reader = KoswatSectionScenarioListJsonDirReader()
        _test_file = test_data.joinpath("acceptance", "scenarios", "10-1-1-A-1-A.json")
        assert _test_file.exists()

        # 2. Run test.
        _scenario_fom = _reader._get_scenario(_test_file)

        # 3. Verify expectations.
        assert isinstance(_scenario_fom, KoswatSectionScenariosJsonFom)
        assert _scenario_fom.scenario_dike_section == _test_file.stem

    def test_read_without_dir(self):
        _result = KoswatSectionScenarioListJsonDirReader().read(Path("not_a_dir"))
        assert _result == []

    def test_read(self):
        # 1. Define test data
        _reader = KoswatSectionScenarioListJsonDirReader(
            dike_selection=["10-1-1-A-1-A"]
        )
        _test_dir = test_data.joinpath("acceptance", "scenarios")
        assert _test_dir.exists()

        # 2. Run test.
        _list_fom = _reader.read(_test_dir)

        # 3. Verify expectations.
        assert any(_list_fom)
        assert all(
            isinstance(_fom, KoswatSectionScenariosJsonFom) for _fom in _list_fom
        )
