# KOSWAT

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3135/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![ci-install-package](https://github.com/Deltares/Koswat/actions/workflows/ci_installation.yml/badge.svg)](https://github.com/Deltares/Koswat/actions/workflows/ci_installation.yml)
![TeamCity build status](https://dpcbuild.deltares.nl/app/rest/builds/buildType:id:Koswat_ContinuousIntegrationBuild_RunFastTests/statusIcon.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Deltares_Koswat&metric=alert_status&token=87fdd0648c19800b4b5fc11334461a7fb602bf20)](https://sonarcloud.io/summary/new_code?id=Deltares_Koswat)
[![GitHub Pages documentation](https://github.com/Deltares/koswat/actions/workflows/deploy_docs.yml/badge.svg)](https://github.com/Deltares/koswat/actions/workflows/deploy_docs.yml)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Deltares/koswat/jupyter-binder)
<!-- ![GitHub release (latest by date)](https://img.shields.io/github/v/release/Deltares/Koswat)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Deltares/Koswat) -->
<!-- [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Deltares/Koswat?quickstart=1) -->

Quick documentation reference:
- [Contributing wiki page](https://github.com/Deltares/Koswat/wiki/Contributing)
- [Installation](https://deltares.github.io/Koswat/installation.html)
- [User manual](https://deltares.github.io/Koswat/usage.html)
    - [Examples](https://deltares.github.io/Koswat/examples.html)
- [Docker](https://deltares.github.io/Koswat/docker.html)

## Features

- Dike profile generation based on data from the koswat `json` file.
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
