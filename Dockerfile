# To build this docker run:
# `docker build -t koswat`

FROM python:3.13

RUN apt-get update

# Copy the directories with the local koswat.
WORKDIR /koswat_src
COPY README.md LICENSE pyproject.toml /koswat_src/
COPY koswat /koswat_src/koswat

# Install the required packages
RUN pip install koswat
RUN apt-get clean autoclean

# Define the endpoint
CMD ["python3"]