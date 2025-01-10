from os import getcwd
from pathlib import Path
from shutil import copy2, copytree, rmtree

_tests_dir = Path(getcwd()).joinpath("tests")
_test_data_path = _tests_dir.joinpath("test_data", "acceptance_reference_data")
_test_results_path = _tests_dir.joinpath("test_results", "sandbox_acceptance_case")

_test_result_folders = [f for f in _test_results_path.iterdir() if f.is_dir()]

for _from_dir in _test_result_folders:
    _to_dir = Path(_test_data_path.joinpath(_from_dir.name))
    _to_dir.mkdir(parents=True, exist_ok=True)

    # Copy CSVs
    for _result_file in list(_from_dir.glob("*.csv")):
        if _result_file.is_file():
            copy2(_result_file, _to_dir)

    # Copy figures
    _from_fig_dir = _from_dir.joinpath("figures")
    _to_fig_dir = _to_dir.joinpath("figures")
    _to_fig_dir.mkdir(parents=True, exist_ok=True)
    if _from_fig_dir.exists():
        rmtree(_to_fig_dir)
        copytree(_from_fig_dir, _to_fig_dir)
