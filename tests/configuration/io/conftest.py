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
