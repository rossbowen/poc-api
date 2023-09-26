import json
from datetime import datetime, timezone

import rdflib
from rdflib import Literal, URIRef
from rdflib.namespace import DCAT, DCTERMS, FOAF, RDF, XSD
from pyld import jsonld
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from poc_api import schemas
from poc_api.context import (
    CONTEXT,
    replace_context_with_remote,
    replace_context_with_local,
)
from poc_api.queries import (
    construct_dataset_core,
    construct_dataset_keywords,
    construct_dataset_themes,
    construct_dataset_contact_point,
    construct_dataset_temporal_coverage,
    construct_edition_core,
    construct_edition_distribution,
)


def create_catalog_record(db: rdflib.Dataset, dataset_id: str):
    """Create a new catalog record with the given metadata."""
    graph = db.get_context(
        URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record")
    )

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # fmt: off
    graph.add((URIRef(f"https://data.ons.gov.uk/catalogue"), DCAT.record, DCAT.CatalogRecord))
    graph.add((URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record"), RDF.type, DCAT.CatalogRecord))
    graph.add((URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record"), FOAF.primaryTopic, URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}")))
    graph.add((URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record"), DCTERMS.created, Literal(now, datatype=XSD.dateTime)))
    # fmt: on


def get_dataset(db: rdflib.Dataset, dataset_id: str) -> dict:
    """Get a dataset by its ID and return its metadata as a JSON-LD dict."""
    graph = db.get_context(
        URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record")
    )
    result = (
        construct_dataset_core(graph)
        + construct_dataset_keywords(graph)
        + construct_dataset_themes(graph)
        + construct_dataset_contact_point(graph)
        + construct_dataset_temporal_coverage(graph)
    )

    res = json.loads(result.serialize(format="json-ld"))

    # If no data is returned from the constructs, return None, which indicates
    # that the dataset does not exist.
    if res == []:
        return None

    res = jsonld.frame(res, {"@context": CONTEXT, "@type": "dcat:DatasetSeries"})
    res = replace_context_with_remote(res)
    return res


def get_datasets():
    pass


def create_dataset(db: rdflib.Dataset, dataset_id: str, dataset: schemas.DatasetCreate):
    """Create a new dataset with the given ID and metadata."""
    data = jsonable_encoder(dataset)
    data = replace_context_with_local(data)

    db.get_context(
        URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record")
    ).parse(data=json.dumps(data), format="json-ld")

    create_catalog_record(db, dataset_id)

    return get_dataset(db, dataset_id)


def delete_dataset(db: rdflib.Dataset, dataset_id: str):
    """Delete a dataset by its ID."""
    db.remove_graph(URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record"))


def get_edition(db: rdflib.Dataset, dataset_id: str, edition_id: str) -> dict:
    graph = db.get_context(
        URIRef(
            f"https://data.ons.gov.uk/datasets/{dataset_id}/editions/{edition_id}/record"
        )
    )
    result = construct_edition_core(graph) + construct_edition_distribution(graph)

    res = json.loads(result.serialize(format="json-ld"))

    # If no data is returned from the constructs, return None, which indicates
    # that the dataset does not exist.
    if res == []:
        return None

    res = jsonld.frame(res, {"@context": CONTEXT, "@type": "dcat:Dataset"})
    res = replace_context_with_remote(res)
    print(res)
    return res


def get_editions():
    pass


def create_edition():
    pass


def delete_edition():
    pass


def get_version():
    pass


def get_versions():
    pass


def delete_version():
    pass
