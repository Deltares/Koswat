# Getting Started

- [Installation](#installation)
    - [Python installation](#python-installation)
    - [Docker installation](#docker-installation)
- [Using Koswat](#using-koswat)
    - [Command line tool](#command-line-tool)
    - [Sandbox](#as-a-sandbox)
    - [Docker](#with-docker)
- [Examples (external)](#examples)

## Installation

### Python installation

!!! Important
    The following installation steps are written based on a Windows environment. When using other systems (which should be possible) it might be required to use different commands. However, the fundamental of the installation steps should remain the same. This meaning, no additional packages or libraries should be required. If problems would arose during your installation, please contact the maintainers of the tool.

#### Requirements

Ensure you have a valid python environment with pip. If you are using conda you can do so with the following command:

```console
conda create -n koswat_env python==3.13 pip
```
!!! note
    At the time of writing of this document koswat is supported for `python>=3.11,<3.14`.

### Pypi Installation

Koswat is published at [Pypi](https://pypi.org/), you can decide to install a concrete version or the latest available from [Pypi](https://pypi.org/project/koswat/#history):

1. Latest available:
    ```bash
    pip install koswat
    ```

2. Concrete version:
    ```bash
    pip install koswat=={version_number}
    ```

An alternative to installing from pypi is to do so via our [Koswat repository](https://github.com/Deltares/Koswat):

1. Latest available (`master`):
    ```bash
    pip install git+https://github.com/Deltares/Koswat.git
    ```

2. Specific Koswat version, add `@version-tag` ([check released tags](https://github.com/Deltares/Koswat/tags)) to the previous command, for instance install tag `v0.15.0`:
    ```bash
    pip install git+https://github.com/Deltares/Koswat.git@v0.15.0
    ```
!!! note
    You can also do the above with a commit-hash for development branches (e.g.:`06e3f27`)


Either way, installation should start immediately:

```console
C:\your_checkout_dir>pip install git+https://github.com/Deltares/Koswat.git
Collecting git+https://github.com/Deltares/Koswat.git
...
Successfully built koswat
Installing collected packages: pytz, tzdata, six, pyshp, pyparsing, pillow, packaging, numpy, more-itertools, kiwisolver, fonttools, cycler, colorama, certifi, shapely, python-dateutil, pyproj, pyogrio, contourpy, click, pandas, matplotlib, geopandas, koswat
Successfully installed certifi-2025.11.12 click-8.3.1 colorama-0.4.6 contourpy-1.3.3 cycler-0.12.1 fonttools-4.60.1 geopandas-1.1.1 kiwisolver-1.4.9 koswat-0.15.0 matplotlib-3.10.7 more-itertools-10.8.0 numpy-2.3.5 packaging-25.0 pandas-2.3.3 pillow-12.0.0 pyogrio-0.11.1 pyparsing-3.2.5 pyproj-3.7.2 pyshp-3.0.2.post1 python-dateutil-2.9.0.post0 pytz-2025.2 shapely-2.1.2 six-1.17.0 tzdata-2025.2
```

Let's verify the installation with `pip show koswat`:

```shell
C:\your_checkout_dir>pip show koswat
Name: koswat
Version: 0.15.0
Summary: Koswat, from the dutch combination of words `Kosts-Wat` (what are the costs). Analyzes all the possible dikes reinforcements based on a provided traject, with surrounding constructions, and what their related costs will be.
...
```

### Docker installation

Koswat can also be used via command line tool with [docker](https://www.docker.com/) or [podman](https://podman.io/). To do so you will have first to [build the image](#build-koswat-docker-image) and then [run the built container](#with-docker).

!!! note
    This guideline assumes you have a podman installation, when using docker you only need to replace our `podman` command with `docker`.

#### Build koswat docker image

The koswat container needs to be built before we can run it, this is not strictly necessary when running a remote image (check [the following step](#with-docker)), but we will check either way how to build either a local or a remote image.

- From a local koswat checkout:
    ```console
    cd {your_local_koswat_checkout}
    podman build -t koswat .
    ```

- From our Deltares registry (as mentioned this step is not really needed):
```console
podman pull containers.deltares.nl/gfs/koswat:latest
```

## Using Koswat

### Requirements

This guideline assumes you have installed koswat, otherwise please check our [installation section](#installation)

### Command line tool

#### Run

When using `Koswat` as a package you can run it directly from the command line as follows:

```console
python -m koswat --input_file path\\to\\your\\koswat.json --log_output path\\to\\your\\output\\dir
```
The arguments are:

- `--input_file` (required): Absolute path to the location of your general `koswat.json` file.
- `--log_output` (optional): Absolute path to the location of where the `koswat.log` will be written. If not specified it will be written at the root of the execution directory.

Check our [examples section](#examples) for more details.

#### --version

You can verify the installed koswat version as:

```console
C:\> python -m koswat --version
python -m koswat, version 0.15.0   
```

#### --help

It is also possible to check all the above possibilities via the `--help` argument in the command line:

```console
C:\> python -m koswat --help
Usage: python -m koswat [OPTIONS] COMMAND [ARGS]...

  CLI call to execute a Koswat analysis given a settings files (`input_file`).
  The log is generated by default in the execute path, unless otherwise
  specified in the `log_output` argument.

  Args:     input_file (str): Location of the `*.json` file containing the
  execution settings for Koswat.     log_output (str): Optional argument to
  specify where will be created the `koswat.log` file.

Options:
  --input_file TEXT  Full path to the config input file.
  --log_output TEXT  Directory location where to generate the Koswat log file.
  --version          Show the version and exit.
  --help             Show this message and exit.
```

### As a sandbox
It is entirely possible to make a custom Koswat analysis using the tool as a sandbox. This means, through a script calling the different classes to generate an analysis.

As a simple example, we can rewrite the acceptance test `test_given_surrounding_files_run_calculations_for_all_included_profiles`:

```python
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.profile import KoswatProfileBase, KoswatProfileBuilder
from koswat.cost_report.summary import KoswatSummary, KoswatSummaryBuilder
from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.cost_report.io.summary.koswat_summary_exporter import KoswatSummaryExporter
from koswat.cost_report.io.plots.multi_location_profile_comparison_plot_exporter import (
    MultiLocationProfileComparisonPlotExporter,
)
from koswat.dike_reinforcements import ReinforcementProfileBuilderFactory

# 1. Define input data.
_input_dir = Path("C:\\my_koswat_input_dir")
_output_dir = Path("C:\\my_koswat_results")
_shp_trajects_file = (
    _input_dir
    / "Dijkvak"
    / "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp"
)
assert _shp_trajects_file.is_file()

## Define input profile case
input_profile_case = KoswatInputProfileBase()
input_profile_case.dike_section = "test_data"
input_profile_case.waterside_ground_level = 0
input_profile_case.waterside_slope = 3
input_profile_case.waterside_berm_width = 0
input_profile_case.waterside_berm_height = 0
input_profile_case.crest_height = 6
input_profile_case.crest_width = 5
input_profile_case.polderside_slope = 3
input_profile_case.polderside_berm_height = 0
input_profile_case.polderside_berm_width = 0
input_profile_case.polderside_ground_level = 0
input_profile_case.pleistocene = -5
input_profile_case.aquifer = -2

## Define the scenario case
scenario_case = KoswatScenario()
scenario_case.scenario_name = ""
scenario_case.scenario_section = ""
scenario_case.d_h = 1
scenario_case.d_s = 10
scenario_case.d_p = 30
scenario_case.crest_width = 5
scenario_case.waterside_slope = 3

## Define the layers case
layers_case = dict(
        base_layer=dict(material=KoswatMaterialType.SAND),
        coating_layers=[
            dict(material=KoswatMaterialType.GRASS, depth=0.3),
            dict(material=KoswatMaterialType.CLAY, depth=0.5),
        ],
    )

## Import surroundings (TODO: update with latest implementation of SurroundingsWrapperCollectionImporter)
_surroundings_importer = KoswatSurroundingsImporter()
_surroundings_importer.traject_loc_shp_file = _shp_trajects_file
_surroundings = _surroundings_importer.import_from(_test_dir)[0]

assert isinstance(scenario_case, KoswatScenario)
_base_koswat_profile = KoswatProfileBuilder.with_data(
    dict(
        input_profile_data=input_profile_case,
        layers_data=layers_case,
        profile_type=KoswatProfileBase,
    )
).build()

## Define the run settings based on the previous calculated parameters.
_run_settings = KoswatRunScenarioSettings()
_run_settings.scenario = scenario_case
_run_settings.surroundings = _surroundings
_run_settings.input_profile_case = _base_koswat_profile

# 2. Run summary
_multi_loc_multi_prof_cost_builder = KoswatSummaryBuilder()
_multi_loc_multi_prof_cost_builder.run_scenario_settings = _run_settings
_summary = _multi_loc_multi_prof_cost_builder.build()

KoswatSummaryExporter(
    koswat_summary=_summary,
    export_path=_output_dir,
    export_shapefiles=False
).export()

# 3. Generate plots
assert isinstance(_summary, KoswatSummary)
assert any(_summary.locations_profile_report_list)
for (
    _reinforcement_profile
) in ReinforcementProfileBuilderFactory.get_available_reinforcements():
    assert any(
        isinstance(
            _rep_profile.profile_cost_report.reinforced_profile,
            _reinforcement_profile,
        )
        for _rep_profile in _summary.locations_profile_report_list
    ), f"Profile type {_reinforcement_profile.__name__} not found."
for _multi_report in _summary.locations_profile_report_list:
    _mlp_plot = MultiLocationProfileComparisonPlotExporter()
    _mlp_plot.cost_report = _multi_report
    _mlp_plot.export_dir = _output_dir
    _mlp_plot.export_measures_png = True
    _mlp_plot.export_layers_png = True
    _mlp_plot.export()

```

### With Docker

Assuming you correctly [installed koswat docker container](#docker-installation), you can now proceed to run the tool, we will make use of our example data ( `examples/basic_case` ), so you can copy it to a local test directory (`{your_data_to_run_directory}`).

Running through docker requires that we **mount** the model data that we will use, this is done with the flag `-v {your_data_location}:/{mounted_data_location}`. 

!!! important
    Make sure all the paths defined in the `koswat_general.json` are relative to it. Otherwise __it will not work__.

- With your local image:
    ```console
    podman run -it -v {your_data_to_run_directory}:/run_data koswat --input_file /run_data/koswat_general.json
    ```
- Or using the remote image instead:
    ```console
    podman run -it -v {your_data_to_run_directory}:/run_data containers.deltares.nl/gfs/koswat:latest --input_file /run_data/koswat_general.json
    ```

Which will result in something like this:
```console
{date and time} - [koswat_handler.py:119] - root - INFO - Initialized Koswat.                                                                                             
{date and time} - [koswat_run_settings_importer.py:70] - root - INFO - Importing CSV configuration from /test_data/koswat_general.json                                     
{date and time} - [koswat_costs_importer.py:41] - root - INFO - Importing costs settings from /test_data/koswat_costs.json.                                                
{date and time} - [koswat_run_settings_importer.py:100] - root - INFO - Importing JSON configuration completed.                                                            
{date and time} - [koswat_run_settings_importer.py:103] - root - INFO - Mapping data to Koswat Settings
{date and time} - [koswat_run_settings_importer.py:158] - root - INFO - Creating scenarios for profile 10-1-1-A-1-A.
{date and time} - [koswat_run_settings_importer.py:171] - root - INFO - Created sub scenario Scenario1.
{date and time} - [koswat_run_settings_importer.py:171] - root - INFO - Created sub scenario Scenario2.
{date and time} - [koswat_run_settings_importer.py:140] - root - WARNING - No scenario found for selected section 10-1-2-A-1-A.
{date and time} - [koswat_run_settings_importer.py:140] - root - WARNING - No scenario found for selected section 10-1-3-A-1-B-1.
{date and time} - [koswat_run_settings_importer.py:174] - root - INFO - Finished generating koswat scenarios. A total of 2 scenarios were created.
{date and time} - [koswat_run_settings_importer.py:112] - root - INFO - Settings import completed.
...
{date and time} - [koswat_handler.py:59] - root - INFO - Exported summary results to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:71] - root - INFO - Exported comparison plots to: /test_data/results_output/dike_10-1-1-A-1-A/scenario_scenario2
{date and time} - [koswat_handler.py:123] - root - INFO - Finalized Koswat.
```

## Examples

You can run all our examples in a [koswat binder environment](https://mybinder.org/v2/gh/Deltares/koswat/jupyter-binder), based on the [jupyter-binder](https://github.com/Deltares/Koswat/tree/jupyter-binder?tab=readme-ov-file) long-living branch.

- Simple runs:
    - [Koswat from command line](https://github.com/Deltares/Koswat/blob/jupyter-binder/koswat_run_as_command_line.md)
    - [Koswat as python package](https://github.com/Deltares/Koswat/blob/jupyter-binder/koswat_run_as_python_package.ipynb)

- [Advanced manual](https://github.com/Deltares/Koswat/blob/jupyter-binder/KOSWAT_Handleiding.ipynb)