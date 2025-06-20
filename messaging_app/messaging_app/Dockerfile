FROM python:3.12-bookworm

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
# Ensure output is shown in real time (no buffering)
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install curl (useful for testing or downloading tools)
RUN apt-get update && apt-get install -y curl gcc build-essential python3-dev libpython3-dev

# Copy the uv binary (a fast pip alternative) from another image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the Python dependencies file into the container
COPY requirements.txt .

# Install Python dependencies using uv
RUN uv pip install -r requirements.txt --system

# Copy the rest of the Django project files
COPY . .

EXPOSE 8000

# Run the Django development server on all interfaces, port 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
