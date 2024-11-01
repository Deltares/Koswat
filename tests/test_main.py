import shutil
from pathlib import Path

from click.testing import CliRunner

from koswat import __main__
from tests import test_data, test_results


class TestMain:
    def test_given_invalid_path_raises_value_error(self):
        _invalid_path = "not\\a\\path"
        _cli_arg = f'--input_file "{_invalid_path}"'
        _run_result = CliRunner().invoke(
            __main__.run_analysis,
            _cli_arg,
        )
        assert _run_result.exit_code == 1
        assert FileNotFoundError == type(_run_result.exc_info[1])
        assert _invalid_path == str(_run_result.exc_info[1])

    def test_given_valid_input_succeeds(self):
        """
        NOTE: This test is used as output reference in `koswat_cost_report.md`.
        Keep it in mind when updating the reference data!
        """
        # 1. Define test data.
        _valid_path = test_data.joinpath("acceptance", "koswat_general.ini")
        assert _valid_path.is_file()
        # Ensure we have a clean results dir.
        _results_dir = test_results.joinpath("acceptance")
        if _results_dir.exists():
            shutil.rmtree(_results_dir)
        _results_dir.mkdir(parents=True)

        _cli_arg = f'--input_file "{_valid_path}" --log_output "{_results_dir}"'

        # 2. Run test.
        _run_result = CliRunner().invoke(
            __main__.run_analysis,
            _cli_arg,
        )
        # 3. Verify final expectations.
        assert _run_result.exit_code == 0
        _log: Path = next(_results_dir.glob("*.log"), None)
        assert _log and _log.is_file(), "Log file was not generated."
        assert (
            _log.read_text().find("ERROR") == -1
        ), "ERROR found in the log, run was not succesful."
