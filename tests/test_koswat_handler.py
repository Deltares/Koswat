from pathlib import Path

import pytest

from koswat.koswat_handler import KoswatHandler
from tests import get_test_results_dir, test_data


class TestKoswatHandler:
    def test_koswat_handler_initialize(self):
        _handler = KoswatHandler(None)
        assert isinstance(_handler, KoswatHandler)

    def test_koswat_handler_with_context_handler_initializes_log(
        self, request: pytest.FixtureRequest
    ):
        _results = get_test_results_dir(request)
        assert not any(_results.glob("*.log"))
        with KoswatHandler(_results) as _handler:
            assert isinstance(_handler, KoswatHandler)
            assert any(_results.glob("*.log"))

    def test_koswat_handler_run_analysis_given_valid_data(
        self, request: pytest.FixtureRequest
    ):
        # 1. Define test data.
        _results_dir = get_test_results_dir(request)
        assert not any(_results_dir.glob("*.log"))
        _ini_file = test_data / "acceptance" / "koswat_general.ini"
        assert _ini_file.is_file()

        # 2. Run test.
        with KoswatHandler(_results_dir) as _handler:
            _handler.run_analysis(_ini_file)

        # 3. Verify results.
        _log: Path = next(_results_dir.glob("*.log"), None)
        assert _log and _log.is_file(), "Log file was not generated."
        assert (
            _log.read_text().find("ERROR") == -1
        ), "ERROR found in the log, run was not succesful."
