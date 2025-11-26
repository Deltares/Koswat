# Installation

> [!IMPORTANT]
> The following installation steps are written based on a Windows environment. When using other systems (which should be possible) it might be required to use different commands. However, the fundamental of the installation steps should remain the same. This meaning, no additional packages or libraries should be required. If problems would arose during your installation, please contact the maintainers of the tool.

## Pypi installation

### Preparation

Ensure you have a valid python environment with pip. If you are using conda you can do so with the following command:

```console
conda create -n koswat_env python==3.13 pip
```
> Note: At the time of writing of this document koswat is supported for `python>=3.11,<3.14`.

### Installation

Koswat is not published at a package repository such as [Pypi], however you can install it directly from GitHub as follows:

1. Latest available (`master`):
    ```bash
    pip install git+https://github.com/Deltares/Koswat.git
    ```

2. Specific Koswat version, add `@version-tag` ([check released tags](https://github.com/Deltares/Koswat/tags)) to the previous command, for instance install tag `v0.15.0`:
    ```bash
    pip install git+https://github.com/Deltares/Koswat.git@v0.15.0
    ```
    > You can also do the above with a commit-hash for development branches (e.g.:`06e3f27
 `)


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

## Docker installation

For docker installation (and usage) check [Koswat](docker.md).
