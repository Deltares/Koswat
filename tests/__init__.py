import shutil
from pathlib import Path

from pytest import FixtureRequest

test_data = Path(__file__).parent.joinpath("test_data")
test_data_acceptance = test_data.joinpath("acceptance")
test_results = Path(__file__).parent.joinpath("test_results")

if not test_results.is_dir():
    test_results.mkdir(parents=True)


def get_test_results_dir(request: FixtureRequest) -> Path:
    _test_dir: Path = test_results / request.node.originalname
    if _test_dir.is_dir():
        shutil.rmtree(_test_dir)
    _test_dir.mkdir(parents=True)
    return _test_dir


def get_fixturerequest_case_name(request: FixtureRequest) -> str:
    _case_name_idx = request.node.name.index("[") + 1
    _case_name = (
        request.node.name[_case_name_idx:-1].lower().replace(" ", "_").replace("-", "_")
    )
    return _case_name


def get_testcase_results_dir(request: FixtureRequest) -> Path:
    _case_name = get_fixturerequest_case_name(request)
    _test_dir: Path = test_results / request.node.originalname
    _test_dir = _test_dir / _case_name
    if _test_dir.is_dir():
        shutil.rmtree(_test_dir)
    _test_dir.mkdir(parents=True)
    return _test_dir


def get_custom_testcase_results_dir(request: FixtureRequest, exclude_part: int) -> Path:
    _case_name = get_fixturerequest_case_name(request)
    _part_to_remove = _case_name.split("_")[exclude_part]
    _case_name = (
        _case_name.replace("_" + _part_to_remove, "")
        .replace(_part_to_remove + "_", "")
        .replace(_part_to_remove, "")
    )

    _test_dir: Path = test_results / request.node.originalname
    _test_dir = _test_dir / _case_name
    _test_dir.mkdir(exist_ok=True, parents=True)

    return _test_dir
