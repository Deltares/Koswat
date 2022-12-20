# KOSWAT
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Deltares_Koswat&metric=alert_status&token=87fdd0648c19800b4b5fc11334461a7fb602bf20)](https://sonarcloud.io/summary/new_code?id=Deltares_Koswat)
<!--  These tags won't work while being private.
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Deltares/Koswat)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Deltares/Koswat) -->

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Description

## Installation

### Using pypi.

When you only require the koswat package to be used as a whole, and not for developments, we advise to directly use the latest greatest release, or directly the latest available version from `Master` as follows:

```
pip install git+https://github.com/Deltares/Koswat.git
```


### Development environment.
Checkout the code from github in a directory of your choice. Navigate to it and then install both the environment and the koswat package as follows:
```bash
conda env create -f "environment.yml"
conda activate koswat_env
poetry install
```
