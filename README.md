# KOSWAT
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Deltares_Koswat&metric=alert_status&token=87fdd0648c19800b4b5fc11334461a7fb602bf20)](https://sonarcloud.io/summary/new_code?id=Deltares_Koswat)
<!--  These tags won't work while being private.
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Deltares/Koswat)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Deltares/Koswat) -->
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Description

## Installation

### With pypi

When you only require the koswat package to be used as a whole, and not for developments, we advise to directly use the latest greatest release, or directly the latest available version from `Master` as follows:

```
pip install git+https://github.com/Deltares/Koswat.git
```


### With development environment
Checkout the code from github in a directory of your choice. Navigate to it and then install both the environment and the koswat package as follows:
```bash
conda env create -f "environment.yml"
conda activate koswat_env
poetry install
```

## Usage
 
When using `Koswat` as a package you can run it directly from the command line as follows:

```cli
python -m koswat --input_file path\\to\\your\\koswat.ini --log_output path\\to\\your\\output\\dir
```
The arguments are:
- `--input_file` (required): Absolute path to the location of your general `koswat.ini` file.
- `--log_output` (optional): Absolute path to the location of where the `koswat.log` will be written. If not specified it will be written at the root of the execution directory.