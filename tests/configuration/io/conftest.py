from pathlib import Path
from shutil import rmtree
from typing import Iterator

import pytest

from tests import test_results


@pytest.fixture
def empty_dir() -> Iterator[Path]:
    _temp_dir = test_results.joinpath("temp_empty_dir")
    if _temp_dir.exists():
        rmtree(_temp_dir)
    _temp_dir.mkdir(parents=True, exist_ok=True)

    yield _temp_dir

    rmtree(_temp_dir)


@pytest.fixture
def empty_file() -> Iterator[Path]:
    _temp_dir = test_results
    _temp_dir.mkdir(parents=True, exist_ok=True)
    _temp_file = _temp_dir.joinpath("empty_file.txt")
    if _temp_file.exists():
        _temp_file.unlink()
    _temp_file.touch()

    yield _temp_file

    rmtree(_temp_file)
