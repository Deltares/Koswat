# To build this docker run (from the top checkout dir):
# `docker build -t koswat_dev .devcontainer`
# To run the docker for pytest:
# `docker run -v {your_koswat_checkout_dir}:/usr/src/app/ -t koswat_dev`
# `pixi install`
# `pixi run pytest -m {your_pytest_arguments}`

FROM ghcr.io/prefix-dev/pixi:latest

RUN apt-get update && apt-get install libgl1 -y

ARG SRC_ROOT="/usr/src"

# Set PIXI_HOME to a location inside the source root
ENV PIXI_HOME=$SRC_ROOT/.pixi

# This location needs to be mounted with your koswat checkout:
# -v {your_koswat_checkout_dir}:/usr/src/app
WORKDIR $SRC_ROOT/app

# Define the endpoint
CMD [ "/bin/bash" ]