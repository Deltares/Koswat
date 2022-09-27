
from click.testing import CliRunner

from koswat import main


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
