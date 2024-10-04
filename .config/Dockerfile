# To build this docker run:
# `docker build -t koswat_dev`
# To run the docker for pytest:
# `docker run -v {your_koswat_checkout_dir}:/usr/src/app/ -v {koswat_env_dir}:/usr/src/.env -t koswat_dev`
# `poetry install`
# `poetry run pytest -m {your_pytest_arguments}`

FROM condaforge/miniforge3:latest

RUN apt-get update && apt-get install libgl1 -y

# Install conda environment
WORKDIR /usr/src/app
COPY environment.yml /usr/src/.config/environment.yml

RUN conda init bash \
    && . ~/.bashrc \
    && conda env create -f /usr/src/.config/environment.yml -p /usr/src/.env

# Activate conda environment
RUN echo "export PATH=/usr/src/.env/bin:$PATH" >>  ~/.bashrc
RUN conda init && echo 'conda activate /usr/src/.env' >>  ~/.bashrc

# Define the endpoint
CMD ["bash"]