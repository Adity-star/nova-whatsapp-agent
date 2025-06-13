# Use an appropriate base image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Set environment variables (e.g., set Python to run in unbuffered mode)
ENV PYTHONUNBUFFERED=1

# Install system dependencies for building libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependency management files (pyproject.toml and README.md)
COPY pyproject.toml README.md /app/

# Install the application dependencies
RUN uv pip install --system .

# Copy your application code into the container
COPY src/ /app/

# Define volumes
VOLUME ["/app/data"]

# Expose the port
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["chainlit", "run", "nova_companion/interfaces/chainlit/app.py", "--port", "8000", "--host", "0.0.0.0"]