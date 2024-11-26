# Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN python3 -m venv .env

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]