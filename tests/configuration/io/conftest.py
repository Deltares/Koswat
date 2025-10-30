from pathlib import Path
from shutil import rmtree
from typing import Iterator

import pytest

from tests import test_results


@pytest.fixture
def empty_dir(request: pytest.FixtureRequest) -> Iterator[Path]:
    _temp_dir = test_results.joinpath(request.node.name, "temp_empty_dir")
    if _temp_dir.exists():
        rmtree(_temp_dir)
    _temp_dir.mkdir(parents=True, exist_ok=True)
    assert _temp_dir.is_dir()

    yield _temp_dir

    rmtree(_temp_dir)


@pytest.fixture
def empty_file(request: pytest.FixtureRequest) -> Iterator[Path]:
    _temp_dir = test_results.joinpath(request.node.name)
    _temp_dir.mkdir(parents=True, exist_ok=True)

    _temp_file = _temp_dir.joinpath("temp_empty_file.txt")
    _temp_file.unlink(missing_ok=True)
    _temp_file.touch()

    assert _temp_file.is_file()

    yield _temp_file

    _temp_file.unlink(missing_ok=True)
