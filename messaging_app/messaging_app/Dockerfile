# Use the official Python 3.12 image as the base OS + Python environment
FROM python:3.12-bookworm

# Set environment variables to:
# - prevent Python from writing .pyc files
# - make sure logs are shown immediately (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
# All future commands will run inside /messaging_app
WORKDIR /messaging_app

# Install system packages:
# - curl: for downloading files
# - gcc, build-essential, python3-dev, libpython3-dev: for compiling Python packages that need C
# - uv: a fast dependency installer (like pip but faster)
RUN apt-get update && apt-get install -y \
    curl gcc build-essential python3-dev libpython3-dev \
    && pip install uv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Ensure you copy the right file into the image root
COPY messaging_app/requirements.txt /messaging_app/requirements.txt

# Now install all requirements, including gunicorn
RUN pip install --no-cache-dir gunicorn && pip install --no-cache-dir -r requirements.txt


# Copy the Django entry script (manage.py) into the container
COPY manage.py .

# Copy the Django project code (settings, wsgi, urls, etc.) into the container
COPY messaging_app/ messaging_app/

# Copy the actual Django app folder (models, views, etc.)
# It's one level up from the Dockerfile — so we use `../messaging/`
COPY ../messaging/ messaging/

# Tell Docker to open port 8000 — so external traffic can reach your app
EXPOSE 8000

# The command to run inside the container when it starts:
# 1. Run database migrations
# 2. Start Gunicorn to serve the app on port 8000
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 messaging_app.wsgi:application"]
