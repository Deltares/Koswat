from pathlib import Path

import pytest

invalid_paths_cases = [
    pytest.param(None, id="None given"),
    pytest.param("", id="Empty string given"),
    pytest.param("not\\a\\path", id="Path as string"),
    pytest.param(Path() / "not_a_valid_file", id="Wrong extension"),
]
