FROM python:3.12

# Install the application dependencies.
WORKDIR /app

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/app/.venv/bin/uvicorn", "main:app", "--port", "80", "--host", "0.0.0.0"]