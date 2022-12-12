import pytest
from click.testing import CliRunner

from koswat import main
from tests import test_data


class TestMain:
    def test_given_invalid_path_raises_value_error(self):
        _invalid_path = "not\\a\\path"
        _cli_arg = f'--input_file "{_invalid_path}"'
        _run_result = CliRunner().invoke(
            main.run_analysis,
            _cli_arg,
        )
        assert _run_result.exit_code == 1
        assert FileNotFoundError == type(_run_result.exc_info[1])
        assert _invalid_path == str(_run_result.exc_info[1])

    def test_given_valid_input_succeeds(self):
        # 1. Define test data.
        _valid_path = test_data / "acceptance" / "koswat_general.ini"
        assert _valid_path.is_file()
        _cli_arg = f'--input_file "{_valid_path}"'

        # 2. Run test.
        _run_result = CliRunner().invoke(
            main.run_analysis,
            _cli_arg,
        )

        # 3. Verify final expectations.
        assert _run_result.exit_code == 0
