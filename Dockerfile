# --- Build stage ---FROM ghcr.io/prefix-dev/pixi:latest AS builder
WORKDIR /appCOPY pyproject.toml pixi.lock README.md LICENSE .COPY koswat /app/koswat
# Install dependencies and build packageRUN pixi install --locked -e py313RUN pixi run python -m build
# --- Runtime stage ---FROM python:3.13-slim AS runtime
WORKDIR /app
# System dependencies (only what’s needed)RUN apt-get update && apt-get install -y --no-install-recommends libgl1 && rm -rf /var/lib/apt/lists/*
# Copy built wheel from builderCOPY --from=builder /app/dist/*.whl /tmp/
# Install koswat packageRUN pip install /tmp/*.whl && rm /tmp/*.whl
# Default workdir for data mountingVOLUME /mnt/koswat_dataWORKDIR /mnt/koswat_data
ENTRYPOINT ["python", "-m", "koswat"]CMD ["--help"]
