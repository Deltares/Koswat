# Installation

__Important!__ : The following installation steps are written based on a Windows environment. When using other systems (which should be possible) it might be required to use different commands. However, the fundamental of the installation steps should remain the same. This meaning, no additional packages or libraries should be required. If problems would arose during your installation, please contact the maintainers of the tool.

## For users

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

3. Using [docker](https://www.docker.com/) (requires checking the repository in a directory):
```bash
cd <your koswat checked out directory>
docker build -t koswat:latest -f Dockerimage .
docker run -it koswat bash
```

## For developers
1. Checkout the code from github in a directory of your choice. You can either do this by downloading the source zip or (better) using git, for instance:
    ```bash
    cd C:\repos
    git clone https://github.com/Deltares/Koswat.git koswat
    ```
    | Note, the above steps are based on a Windows setup. If you are not familiar with Git we recommend using the [GitHub desktop tool](https://desktop.github.com/).

2. Navigate to your Koswat repository and then install the koswat package with your preferred step:

    1. With [Miniforge](https://conda-forge.org/miniforge/) (our recommendation):    
        ```bash
        cd C:\repos\koswat
        conda env create -f .devcontainer\environment.yml
        conda activate koswat_env
        poetry install
        ```
    2. With `pypi`:
        ```bash
        cd C:\repos\koswat
        pip install .
        ```
        | Note, this will not install `Poetry`, which is required to properly maintain the interdependencies of `Koswat` tool.