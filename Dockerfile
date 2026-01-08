# Use an official Python runtime as a parent image
FROM python:3.11-slim
# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set work directory
WORKDIR /app
# Install system dependencies (gcc might be needed for some python packages)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
# Install Poetry
RUN pip install poetry
# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/
# Configure poetry to not create a virtual environment inside the container
RUN poetry config virtualenvs.create false
# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi
# Copy project
COPY . /app
# Expose port
EXPOSE 8000
# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]