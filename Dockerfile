# To build this docker run:
# `docker build -t koswat`

# To run koswat in the container:
# `docker run 
#   -v {your_koswat_data_project}:/mnt/koswat_data koswat 
#   --input_file /mnt/koswat_data/koswat_general.json`
# Replace `{your_koswat_data_project}` with the path to your local koswat data project.
# Ensure all the paths within koswat_general.json are relative to (and include) `/mnt/koswat_data/`

FROM python:3.13-slim

# Copy the directories with the local koswat.
COPY README.md LICENSE pyproject.toml /app/
COPY koswat /app/koswat

# Install koswat and its dependencies.
RUN pip install --upgrade pip && pip install /app

# Set the entrypoint to run koswat as a module.
ENTRYPOINT [ "python", "-m", "koswat" ]