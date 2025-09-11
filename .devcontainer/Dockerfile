# To build this docker run (from the top checkout dir):
# `docker build -t koswat_dev .devcontainer`
# To run the docker for pytest:
# `docker run -v {your_koswat_checkout_dir}:/usr/src/app/ -v {koswat_env_dir}:/usr/src/.env -t koswat_dev`
# `poetry install`
# `poetry run pytest -m {your_pytest_arguments}`

FROM condaforge/miniforge3:latest

RUN apt-get update && apt-get install libgl1 -y

ARG SRC_ROOT="/usr/src"

# For persisting the environment remember to mount it as well:
# -v {your_local_tmp_dir}:/usr/src/.env
# ARG CONDA_ENV="${SRC_ROOT}/.env"

# This location needs to be mounted with your koswat checout:
# -v {your_koswat_checkout_dir}:/usr/src/app
WORKDIR $SRC_ROOT/app
COPY environment.yml $SRC_ROOT/.devcontainer/environment.yml

RUN wget -qO- https://pixi.sh/install.sh | sh
ENV PATH="/root/.pixi/bin":$PATH

# Define the endpoint
CMD [ "/bin/bash" ]