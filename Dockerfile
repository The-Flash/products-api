# Dockerfile for FastAPI application

# Use a slim Python image as base
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install uv (if not already installed, as pyproject.toml and uv.lock suggest its usage)
# You might need to adjust this if uv is not desired or installed differently
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI application using uvicorn
# Assuming your FastAPI app instance is named 'app' in main.py
CMD ["uvicorn", "main:app", "--host", "0.0.00", "--port", "8000"]
