from os import getcwd, rmdir, unlink
from pathlib import Path
from shutil import copy2, copytree, rmtree

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

    # Copy figures
    _from_dir = _test_results_path.joinpath(_case.name).joinpath("figures")
    _to_fig_dir = _to_dir.joinpath("figures")
    if _from_dir.exists() and _to_fig_dir.exists():
        rmtree(_to_fig_dir)
        copytree(_from_dir, _to_fig_dir)
