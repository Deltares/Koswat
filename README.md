# KOSWAT
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3135/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![ci-install-package](https://github.com/Deltares/Koswat/actions/workflows/ci_installation.yml/badge.svg)](https://github.com/Deltares/Koswat/actions/workflows/ci_installation.yml)
![TeamCity build status](https://dpcbuild.deltares.nl/app/rest/builds/buildType:id:Koswat_ContinuousIntegrationBuild_RunFastTests/statusIcon.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Deltares_Koswat&metric=alert_status&token=87fdd0648c19800b4b5fc11334461a7fb602bf20)](https://sonarcloud.io/summary/new_code?id=Deltares_Koswat)
<!-- ![GitHub release (latest by date)](https://img.shields.io/github/v/release/Deltares/Koswat)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Deltares/Koswat) -->
<!-- [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Deltares/Koswat?quickstart=1) -->

## Detailed documentation

Currently the detailed documentation is only reachable when building it locally, to do so check the section [read the docs documentation](#read-the-docs-documentation).

## Features

- Dike profile generation based on data from the koswat `ini` file.
- Calculation of all possible reinforcement profiles.
- Filtering of reinforcement profiles based on their surroundings.
- Cost calculation for added and removed material per layer per reinforcement.
- Plotting of reinforcements and layer cross section.
- Export of results to `csv`.
- Logging of analysis.

## Intended audience
Koswat targets two types of users:
- Sandbox users. This target group are users acquianted with `Python` scripting. For them we envision two main interests when using the tool as a sandbox:
    - Extending its functionality, or _correcting_ the existing one via pull-requests. This requires them to adhere to our __Development Guidelines__ (not yet present) and to use the Koswat repository in [Development mode](#development-mode).
    - Creating their own scripts. It is possible to use the full extent of Koswat features on custom scripts, of course under your own responsibility. In this case the user only requires to install the most convinient version of the package as a [sandbox / endpoint](#sandbox--endpoint).
- Single endpoint users. These users are only interested in running the tool via command line or other User Interfaces. For them, it is advised to install the tool as a [sandbox / endpoint](#sandbox--endpoint) and to check the tool's [endpoint usage](#endpoint-usage).


## Installation

__Important!__ The following installation steps are written based on a Windows environment. When using other systems (which should be possible) it might be required to use different commands. However, the fundamental of the installation steps should remain the same. This meaning, no additional packages or libraries should be required. If problems would arose during your installation, please contact the maintainers of the tool.

### Sandbox / Endpoint

When you only require the koswat package to be used as a whole, and not for developments, we advise to directly use the latest greatest release, or directly the latest available version from `Master` as follows:

1. Latest available `Master`:
```console
pip install git+https://github.com/Deltares/Koswat.git
```

2. Specific Koswat version, add `@version-tag` to the previous command, for instance install tag `v0.11.0` (__MVP__ pre-release):
```console
pip install git+https://github.com/Deltares/Koswat.git@v0.11.0
```
| You can also do the above with a commit-hash for development branches (e.g.:`@0504c06`)



### Development mode

Please check our related [contributing wiki page](https://github.com/Deltares/Koswat/wiki/Contributing)

#### Read the docs documentation.

Documentation for the project is currently only available with a manual step. You can do this if you installed the project following the steps of the [development mode](#development-mode). Then execute the `MkDocs` build and serve step:
```console
poetry run mkdocs build
poetry run mkdocs serve
```

## Endpoint usage
 
### As a package
When using `Koswat` as a package you can run it directly from the command line as follows:

```console
python -m koswat --input_file path\\to\\your\\koswat.ini --log_output path\\to\\your\\output\\dir
```
The arguments are:
- `--input_file` (required): Absolute path to the location of your general `koswat.ini` file.
- `--log_output` (optional): Absolute path to the location of where the `koswat.log` will be written. If not specified it will be written at the root of the execution directory.

It is also possible to check all the above possibilities via the `--help` argument in the command line:
```console
python -m koswat --help
```

### Podman / docker

1. First you need to build the koswat docker image by any of the following two ways:

- You can either it from a local checkout:
    ```console
    podman build -t koswat .
    ```

- Or from our Deltares registry (although this step is not really needed):
    ```console
    podman pull containers.deltares.nl/gfs/koswat:latest
    ```

2. You can now proceed to run the tool, we will make use of our test data ( `tests/test_data/acceptance` ), so you can copy it to a local test directory (`{your_data_to_run_directory}`):

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
{date and time} - [koswat_run_settings_importer.py:70] - root - INFO - Importing INI configuration from /test_data/koswat_general.json                                
{date and time} - [koswat_costs_importer.py:41] - root - INFO - Importing costs settings from /test_data/koswat_costs.json.                                                
{date and time} - [koswat_run_settings_importer.py:100] - root - INFO - Importing INI configuration completed.                                                            
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

> [!IMPORTANT]
> At the moment this docker requires that all the paths defined in the `koswat_general.json` are relative to the mounted data. So in our case we  had to modify them such as `Dijksecties_Selectie = /run_data/koswat_dike_selection.txt` and so on for each of them.
> Otherwise it will not work.
