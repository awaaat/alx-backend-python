FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /messaging_app

RUN apt-get update && apt-get install -y \
    curl gcc build-essential python3-dev libpython3-dev \
    && pip install uv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY messaging_app/requirements.txt .

RUN uv pip install -r requirements.txt --system

COPY . .

RUN ls -la /messaging_app  # Debug: Confirm manage.py is present

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]