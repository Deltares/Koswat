import pytest
from typing import List
from click.testing import CliRunner
from koswat import main

class TestMain:

    def test_given_invalid_path_raises_value_error(
        self):
        _invalid_path = "not//a//path"
        _expected_err = ""
        with pytest.raises(FileNotFoundError) as exc_err:
            _run_result = CliRunner().invoke(
                main.run_analysis,
                _invalid_path,
            )
        assert str(exc_err.value) == _invalid_path