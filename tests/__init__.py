import shutil
from pathlib import Path

from pytest import FixtureRequest

test_data = Path(__file__).parent / "test_data"
test_results = Path(__file__).parent / "test_results"

if not test_results.is_dir():
    test_results.mkdir(parents=True)


def get_fixturerequest_case_name(request: FixtureRequest):
    _case_name_idx = request.node.name.index("[") + 1
    _case_name = (
        request.node.name[_case_name_idx:-1].lower().replace(" ", "_").replace("-", "_")
    )
    return _case_name


def get_testcase_results_dir(request: FixtureRequest) -> Path:
    _case_name = get_fixturerequest_case_name(request)
    _test_dir: Path = test_results / request.node.originalname
    _test_dir.mkdir(exist_ok=True, parents=True)
    _test_dir = _test_dir / _case_name
    if _test_dir.is_dir():
        shutil.rmtree(_test_dir)
    _test_dir.mkdir(parents=True)
    return _test_dir
