# KOSWAT
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3135/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
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
```bash
pip install git+https://github.com/Deltares/Koswat.git
```

2. Specific Koswat version, add `@version-tag` to the previous command, for instance install tag `v0.11.0` (__MVP__ pre-release):
```bash
pip install git+https://github.com/Deltares/Koswat.git@v0.11.0
```
| You can also do the above with a commit-hash for development branches (e.g.:`@0504c06`)



### Development mode

Please check our related [contributing wiki page](https://github.com/Deltares/Koswat/wiki/Contributing)

#### Read the docs documentation.

Documentation for the project is currently only available with a manual step. You can do this if you installed the project following the steps of the [development mode](#development-mode). Then execute the `MkDocs` build and serve step:
```cli
poetry run mkdocs build
poetry run mkdocs serve
```

## Endpoint usage
 
When using `Koswat` as a package you can run it directly from the command line as follows:

```cli
python -m koswat --input_file path\\to\\your\\koswat.ini --log_output path\\to\\your\\output\\dir
```
The arguments are:
- `--input_file` (required): Absolute path to the location of your general `koswat.ini` file.
- `--log_output` (optional): Absolute path to the location of where the `koswat.log` will be written. If not specified it will be written at the root of the execution directory.

It is also possible to check all the above possibilities via the `--help` argument in the command line:
```cli
python -m koswat --help
```