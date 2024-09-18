from os import getcwd
from pathlib import Path
from shutil import copy2

_test_data_path = Path(getcwd()).joinpath(r"tests\test_data\acceptance_reference_data")
_test_results_path = Path(getcwd()).joinpath(
    r"tests\test_results\sandbox_acceptance_case"
)
_costs_filename = "summary_costs.csv"
_locations_filename = "summary_locations.csv"

_test_data_folders = [f for f in _test_data_path.iterdir() if f.is_dir()]

for _case in _test_data_folders:
    _to_dir = Path(_test_data_path.joinpath(_case))

    _from_file = Path(_test_results_path.joinpath(_case.name).joinpath(_costs_filename))
    if _from_file.exists() and _to_dir.exists():
        copy2(_from_file, _to_dir)

    _from_file = _test_results_path.joinpath(_case.name).joinpath(_locations_filename)
    if _from_file.exists() and _to_dir.exists():
        copy2(_from_file, _to_dir)
