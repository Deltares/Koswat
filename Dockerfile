# To build this docker run:
# `docker build -t koswat`

# To run koswat in the container:
# `docker run 
#   -v {your_koswat_data_project}:/mnt/koswat_data koswat 
#   --input_file /mnt/koswat_data/koswat_general.ini`

FROM ghcr.io/prefix-dev/pixi:latest as BUILD

RUN apt-get update && apt-get install libgl1 -y

# Copy the directories with the local koswat.
WORKDIR /koswat_src
COPY README.md LICENSE pyproject.toml pixi.lock /koswat_src/
COPY koswat /koswat_src/koswat

# Install the python=3.13 environment
RUN pixi install --locked -e py313 && pixi shell -e py313
RUN pixi add pip && pixi run pip list --format=freeze > requirements.txt

FROM python:3.13-slim

WORKDIR /app
COPY --from=BUILD /koswat_src/ /app

RUN pip install -r requirements.txt
RUN pip install .

# Define the endpoint
CMD ["koswat", "--help"]