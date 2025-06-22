FROM python:3.12-bookworm

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
# Ensure output is shown in real time (no buffering)
    PYTHONUNBUFFERED=1

# Install curl and dependencies, then install uv
RUN apt-get update && apt-get install -y curl gcc build-essential python3-dev libpython3-dev && pip install uv
# Copy the uv binary (a fast pip alternative) from another image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Copy the Python dependencies file into the container
COPY messaging_app/requirements.txt .
COPY . /app/

# Install Python dependencies using uv
RUN uv pip install -r requirements.txt --system

EXPOSE 8000

# Run the Django development server on all interfaces, port 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata seed && python manage.py runserver 0.0.0.0:8000"]