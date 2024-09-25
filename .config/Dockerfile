# To build this docker run:
# `docker build -t koswat_dev`
# To run the docker for pytest:
# `docker run -v {your_koswat_checkout_dir}:/koswat_checkout -t koswat_dev`
# `cd /koswat_checkout`
# `conda env create -f .config/environment.yml -p .koswat_env`
# `poetry install`
# `poetry run pytest -v {your_pytest_arguments}`

FROM condaforge/miniforge3:latest

RUN apt-get update && apt-get install libgl1 -y

# Define the endpoint
CMD ["bash"]