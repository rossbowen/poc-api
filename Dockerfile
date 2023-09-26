FROM python:3.11 as requirements-stage

WORKDIR /tmp
RUN pip install poetry
COPY ./api/pyproject.toml ./api/poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11

WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./api /app
ENV PYTHONPATH=/app/src

CMD ["uvicorn", "poc_api.main:app", "--host", "0.0.0.0", "--port", "80"]