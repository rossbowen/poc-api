A proof of concept API using FastAPI and Oxigraph. Uses poetry for packaging.

- `/api` contains the API code
- `/data` contains Oxigraph data

```sh
docker compose run oxigraph
```

```sh
cd api
poetry install
poetry run uvicorn poc_api.main:app --host 0.0.0.0 --port 8080 --reload
```

Data can be seeded into the database by running `/api/src/seed/seed.py`.