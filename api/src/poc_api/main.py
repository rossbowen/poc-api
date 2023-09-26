"""https://fastapi.tiangolo.com/tutorial/sql-databases/"""

import rdflib
from fastapi import Depends, File, FastAPI, HTTPException, UploadFile
from google.cloud import storage

from poc_api import crud, database, schemas

app = FastAPI()

# TODO: Respond with a 500 if the database is not available


def get_db():
    try:
        db = database.db
        return db
    finally:
        db.close()


@app.get("/datasets", response_model=list[schemas.Dataset])
def read_datasets(
    skip: int = 0, limit: int = 100, db: rdflib.Dataset = Depends(get_db)
):
    db_datasets = crud.get_datasets(db, skip=skip, limit=limit)
    return db_datasets


@app.get(
    "/datasets/{dataset_id}",
    response_model=schemas.Dataset,
    response_model_exclude_none=True,
)
def read_dataset(dataset_id: str, db: rdflib.Dataset = Depends(get_db)):
    db_dataset = crud.get_dataset(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset


@app.get(
    "/datasets/{dataset_id}/latest",
    response_model=schemas.Dataset,
    response_model_exclude_none=True,
)
def read_latest_dataset(dataset_id: str, db: rdflib.Dataset = Depends(get_db)):
    db_dataset = crud.get_dataset(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset


@app.post("/datasets/{dataset_id}", response_model=schemas.Dataset)
def create_dataset(
    dataset_id: str,
    dataset: schemas.DatasetCreate,
    db: rdflib.Dataset = Depends(get_db),
):
    db_dataset = crud.get_dataset(db, dataset_id=dataset_id)
    if db_dataset:
        raise HTTPException(status_code=400, detail="Dataset already exists")
    db_dataset = crud.create_dataset(db, dataset_id=dataset_id, dataset=dataset)
    return db_dataset


@app.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: str, db: rdflib.Dataset = Depends(get_db)):
    db_dataset = crud.get_dataset(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    db_dataset = crud.delete_dataset(db, dataset_id=dataset_id)


@app.get("/datasets/{dataset_id}/editions/{edition_id}", response_model=schemas.Edition)
def read_edition(
    dataset_id: str,
    edition_id: str,
    db: rdflib.Dataset = Depends(get_db),
):
    db_edition = crud.get_edition(db, dataset_id=dataset_id, edition_id=edition_id)
    if db_edition is None:
        raise HTTPException(status_code=404, detail="Edition not found")
    return db_edition


@app.get("/datasets/{dataset_id}/editions", response_model=list[schemas.Edition])
def read_editions(
    dataset_id: str,
    skip: int = 0,
    limit: int = 100,
    db: rdflib.Dataset = Depends(get_db),
):
    db_editions = crud.get_editions(db, dataset_id=dataset_id, skip=skip, limit=limit)
    return db_editions


@app.post(
    "/datasets/{dataset_id}/editions/{edition_id}",
    response_model=schemas.Edition,
)
def create_edition(
    dataset_id: str,
    edition_id: str,
    edition: schemas.EditionCreate,
    db: rdflib.Dataset = Depends(get_db),
):
    db_edition = crud.get_edition(db, dataset_id=dataset_id, edition_id=edition_id)
    if db_edition:
        raise HTTPException(status_code=400, detail="Edition already exists")
    db_edition = crud.create_edition(
        db, dataset_id=dataset_id, edition_id=edition_id, edition=edition
    )
    return db_edition

@app.get("/topics")
def read_topics():
    pass

@app.get("/topics")
def read_publishers():
    pass