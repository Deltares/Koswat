from pathlib import Path

import pytest

from koswat.koswat_handler import KoswatHandler
from tests import get_test_results_dir, test_data, test_results

log_filter = "*.log"


class TestKoswatHandler:
    def test_koswat_handler_initialize(self):
        _handler = KoswatHandler(None)
        assert isinstance(_handler, KoswatHandler)

    def test_koswat_handler_with_context_handler_initializes_log(
        self, request: pytest.FixtureRequest
    ):
        _results = get_test_results_dir(request)
        assert not any(_results.glob(log_filter))
        with KoswatHandler(_results) as _handler:
            assert isinstance(_handler, KoswatHandler)
            assert any(_results.glob(log_filter))

    def test_koswat_handler_run_analysis_given_valid_data(
        self, request: pytest.FixtureRequest
    ):
        # 1. Define test data.
        _results_dir = get_test_results_dir(request)
        assert not any(_results_dir.glob(log_filter))

        _acceptance_dir = test_data.joinpath("acceptance")
        _config_file = _acceptance_dir.joinpath("koswat_general.json")
        assert _config_file.is_file()

        # 2. Run test.
        with KoswatHandler(_results_dir) as _handler:
            _handler.run_analysis(_config_file)

        # 3. Verify results.
        _log: Path = next(_results_dir.glob(log_filter), None)
        assert _log and _log.is_file(), "Log file was not generated."
        assert (
            _log.read_text().find("ERROR") == -1
        ), "ERROR found in the log, run was not succesful."

        _scenarios_dir = test_results.joinpath(
            "acceptance", "results_output", "dike_10-1-1-A-1-A"
        )
        assert _scenarios_dir.is_dir(), "Scenarios directory was not created."

        for _scenario_dir in ["scenario1", "scenario2"]:
            _scenario_path = _scenarios_dir.joinpath(f"scenario_{_scenario_dir}")
            assert (
                _scenario_path.is_dir()
            ), f"Scenario directory { _scenario_dir } was not created."

            _scenario_1_summary_locations = _scenario_path.joinpath(
                "summary_locations.csv"
            )
            assert (
                _scenario_1_summary_locations.is_file()
            ), "Summary locations file was not created."

            _reference_summary = _acceptance_dir.joinpath(
                "results_reference",
                f"scenario_{_scenario_dir}",
                "summary_locations.csv",
            )

            _result_text = _scenario_1_summary_locations.read_text()
            _reference_text = _reference_summary.read_text()
            assert (
                _result_text == _reference_text
            ), "Summary locations file does not match reference."
