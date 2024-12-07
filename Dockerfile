FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "app.api.endpoints:app", "--host", "0.0.0.0", "--port", "8000"]
