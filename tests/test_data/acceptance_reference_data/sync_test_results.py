from os import getcwd
from pathlib import Path
from shutil import copy2, copytree, rmtree

_test_data_path = Path(getcwd()).joinpath(r"tests\test_data\acceptance_reference_data")
_test_results_path = Path(getcwd()).joinpath(
    r"tests\test_results\sandbox_acceptance_case"
)

_test_result_folders = [f for f in _test_results_path.iterdir() if f.is_dir()]

for _from_dir in _test_result_folders:
    _to_dir = Path(_test_data_path.joinpath(_from_dir.name))

    # Copy CSVs
    for _result_file in list(_from_dir.glob("*.csv")):
        if _result_file.is_file() and _to_dir.exists():
            copy2(_result_file, _to_dir)

    # Copy figures
    _from_fig_dir = _from_dir.joinpath("figures")
    _to_fig_dir = _to_dir.joinpath("figures")
    if _from_fig_dir.exists() and _to_fig_dir.exists():
        rmtree(_to_fig_dir)
        copytree(_from_fig_dir, _to_fig_dir)
