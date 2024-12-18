# What is .devcontainer for?
The purpose of this directory is to contain both the conda environment file (`environment.yml`) as well as a docker image that already has such environment installed and defined as entry point.

## Installing the conda environment.

To use the environment file simply run in your command line, this assumes you have [anaconda (miniforge)](https://conda-forge.org/miniforge/) installed and the binaries added to your `PATH` environment variables:

```cmd
conda env create -f .devcontainer/environment.yml -p .koswat_env
```
> `-f` (--FILE) is the argument to define which file will be used to install the environment.

> `-p` (--PREFIX) is the argument to define **where** to create the environment.

## Installing the DOCKER environment.
You can install the docker image in two ways:

1. Building and running the image yourself.
    
    ```cmd
    docker build -t koswat_dev .devcontainer
    ```

2. Pulling the pre-built image from `containers.deltares.nl/gfs-dev/koswat_dev:latest`.
    ```cmd
    docker pull containers.deltares.nl/gfs-dev/koswat_dev:latest
    ```

And now you can simply run via command line: 
    ```cmd
    docker run -it -v {your_koswat_checkout_dir}:/usr/src/app -v koswat_docker_env:/usr/src/.env koswat_dev /bin/sh -c "poetry config virtualenvs.create false --local && poetry install"
    ```
- `-v {your_koswat_checkout_dir}:/usr/src/app` will mount your koswat checkout directory into a local directory of the docker container.
- `-v {koswat_docker_env:/usr/src/.env` will create a volume that will allow you to persist your conda environment throughout different docker terminals. You may skip this command if you only want a "one time" execution.
- `-c "poetry config virtualenvs.create false --local && poetry install"` Installs the contents of `{your_koswat_checkout_dir}`, **it is required** to disable the virtual creation of environments from `poetry`.