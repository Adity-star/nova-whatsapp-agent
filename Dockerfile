FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency and metadata files
COPY uv.lock pyproject.toml README.md /app/

# Copy the source code to src/, to match pyproject.toml layout
COPY src/ /app/src/

# Create and activate virtual environment
RUN uv venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies and the package in development mode
RUN uv pip install -e .

VOLUME ["/app/data"]
EXPOSE 8080

CMD ["uvicorn", "nova_companion.interfaces.whatsapp.webhook_endpoint:app", "--host", "0.0.0.0", "--port", "8080"]
