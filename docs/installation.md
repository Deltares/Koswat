# Installation

__Important!__ : The following installation steps are written based on a Windows environment. When using other systems (which should be possible) it might be required to use different commands. However, the fundamental of the installation steps should remain the same. This meaning, no additional packages or libraries should be required. If problems would arose during your installation, please contact the maintainers of the tool.

## For users

When you only require the koswat package to be used as a whole, and not for [development](#for-developers), we advise to directly use the latest greatest release, or directly the latest available version from `master`  there are different ways to do so:

1. Latest available `master`:
```bash
pip install git+https://github.com/Deltares/Koswat.git
```

2. Specific Koswat version, add `@version-tag` to the previous command, for instance install tag `v0.11.0` (__MVP__ pre-release):
```bash

pip install git+https://github.com/Deltares/Koswat.git@v0.11.0
```
| You can also do the above with a commit-hash for development branches (e.g.:`@0504c06`)

3. Using [docker](https://www.docker.com/) or [podman](https://podman.io/) (for both is required checking the repository in a directory):
```bash
cd <your koswat checked out directory>
docker build -t koswat:latest -f Dockerimage .
docker run -it koswat bash
```
| For podman installations use the command `podman` instead of `docker`.

## For developers

If you want to contribute to this project please check our [contributing wiki section](https://github.com/Deltares/Koswat/wiki/Contributing).
