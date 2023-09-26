import pytest
import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF, FOAF, DCAT, DCTERMS

from poc_api import crud, schemas


def sort_dict_and_list_keys(d: dict):
    """
    Used to test equivalence of dicts and lists, ignoring order.

    Usage:
        `assert sort_dict_and_lists(a) == sort_dict_and_lists(b)`
    """
    if isinstance(d, dict):
        return {k: sort_dict_and_list_keys(v) for k, v in sorted(d.items())}
    if isinstance(d, list):
        return sorted([sort_dict_and_list_keys(v) for v in d])
    return d


@pytest.fixture
def dataset_user_metadata():
    metadata = {
        "@context": "https://data.ons.gov.uk/ns#",
        "@id": "https://data.ons.gov.uk/datasets/cpih",
        "@type": "dcat:DatasetSeries",
        "identifier": "cpih",
        "title": "Consumer Price Inflation including owner occupiers' housing costs (CPIH)",
        "summary": "The Consumer Prices Index including owner occupiers' housing costs (CPIH) is a measure of inflation which includes the costs associated with owning, maintaining and living in one's own home.",
        "description": "The Consumer Prices Index including owner occupiers' housing costs (CPIH) is a measure of inflation which includes the costs associated with owning, maintaining and living in one's own home. The CPIH is the most comprehensive measure of inflation.",
        "issued_date": "2023-06-21T07:00:00+00:00",
        "next_release_date": "2023-09-20T07:00:00+00:00",
        "publisher": "office-for-national-statistics",
        "creator": "office-for-national-statistics",
        "contact_point": {
            "name": "Consumer Price Inflation Enquiries",
            "email": "mailto:cpi@ons.gov.uk",
        },
        "theme": ["economy", "prices"],
        "frequency": "monthly",
        "keywords": [
            "cpih",
            "consumer price index including owner occupiers' housing costs",
            "cpi",
            "inflation",
            "consumer price index",
            "consumer price inflation",
        ],
        "licence": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        "spatial_coverage": "K02000001",
        "temporal_coverage": {
            "start": "1989-01-01T00:00:00+00:00",
            "end": "2023-08-01T00:00:00+00:00",
        },
        "temporal_resolution": "P1M",
    }
    return metadata


@pytest.fixture
def dataset_response_metadata():
    metadata = {
        "@context": "https://data.ons.gov.uk/ns#",
        "@id": "https://data.ons.gov.uk/datasets/cpih",
        "@type": "dcat:DatasetSeries",
        "identifier": "cpih",
        "title": "Consumer Price Inflation including owner occupiers' housing costs (CPIH)",
        "summary": "The Consumer Prices Index including owner occupiers' housing costs (CPIH) is a measure of inflation which includes the costs associated with owning, maintaining and living in one's own home.",
        "description": "The Consumer Prices Index including owner occupiers' housing costs (CPIH) is a measure of inflation which includes the costs associated with owning, maintaining and living in one's own home. The CPIH is the most comprehensive measure of inflation.",
        "issued_date": "2023-06-21T07:00:00+00:00",
        "next_release_date": "2023-09-20T07:00:00+00:00",
        "publisher": "office-for-national-statistics",
        "creator": "office-for-national-statistics",
        "contact_point": {
            "name": "Consumer Price Inflation Enquiries",
            "email": "mailto:cpi@ons.gov.uk",
        },
        "theme": ["economy", "prices"],
        "frequency": "monthly",
        "keywords": [
            "cpih",
            "consumer price index including owner occupiers' housing costs",
            "cpi",
            "inflation",
            "consumer price index",
            "consumer price inflation",
        ],
        "licence": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        "spatial_coverage": "K02000001",
        "temporal_coverage": {
            "start": "1989-01-01T00:00:00+00:00",
            "end": "2023-08-01T00:00:00+00:00",
        },
        "temporal_resolution": "P1M",
    }
    return metadata


def test_create_catalogue_record():
    """Test that a catalog record can be created."""
    db = rdflib.Dataset()
    dataset_id = "cpih"

    # Create the catalog record
    crud.create_catalog_record(db, dataset_id)

    graph = db.get_context(
        URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record")
    )

    # fmt: off
    assert len(db) == 4
    assert (URIRef(f"https://data.ons.gov.uk/catalogue"), DCAT.record, DCAT.CatalogRecord) in graph
    assert (URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record"), RDF.type, DCAT.CatalogRecord) in graph
    assert (URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record"), FOAF.primaryTopic, URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}")) in graph
    assert (URIRef(f"https://data.ons.gov.uk/datasets/{dataset_id}/record"), DCTERMS.created, None) in graph
    # fmt: on


def test_create_dataset(dataset_user_metadata):
    """Test that a dataset can be created and returned once created."""
    db = rdflib.Dataset()
    dataset = schemas.DatasetCreate(**dataset_user_metadata)
    result = crud.create_dataset(db, "cpih", dataset)

    # Test condition does some sorting of dicts and lists - we're not bothered
    # about the order of the lists (e.g. order of themes or order of keywords)
    assert sort_dict_and_list_keys(result) == sort_dict_and_list_keys(
        dataset_user_metadata
    )


def test_get_dataset(dataset_response_metadata):
    """Test that a dataset can be retrieved."""
    db = rdflib.Dataset()
    data = """
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix dcterms: <http://purl.org/dc/terms/> .
    @prefix ons: <https://data.ons.gov.uk/ns#> .
    @prefix vcard: <http://www.w3.org/2006/vcard/ns#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <https://data.ons.gov.uk/datasets/cpih/record> {
        <https://data.ons.gov.uk/datasets/cpih> a dcat:DatasetSeries ;
            dcterms:abstract "The Consumer Prices Index including owner occupiers' housing costs (CPIH) is a measure of inflation which includes the costs associated with owning, maintaining and living in one's own home."@en ;
            dcterms:accrualPeriodicity <http://purl.org/cld/freq/monthly> ;
            dcterms:creator <https://www.gov.uk/government/organisations/office-for-national-statistics> ;
            dcterms:description "The Consumer Prices Index including owner occupiers' housing costs (CPIH) is a measure of inflation which includes the costs associated with owning, maintaining and living in one's own home. The CPIH is the most comprehensive measure of inflation."@en ;
            dcterms:identifier "cpih" ;
            dcterms:issued "2023-06-21T07:00:00+00:00"^^xsd:dateTime ;
            dcterms:license <http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/> ;
            dcterms:publisher <https://www.gov.uk/government/organisations/office-for-national-statistics> ;
            dcterms:spatial <http://statistics.data.gov.uk/id/statistical-geography/K02000001> ;
            dcterms:temporal _:b1 ;
            dcterms:temporalResolution "P1M"^^xsd:duration ;
            dcterms:title "Consumer Price Inflation including owner occupiers' housing costs (CPIH)"@en ;
            dcat:contactPoint _:b2 ;
            dcat:keyword "consumer price index"@en,
                "consumer price index including owner occupiers' housing costs"@en,
                "consumer price inflation"@en,
                "cpi"@en,
                "cpih"@en,
                "inflation"@en ;
            dcat:theme <https://data.ons.gov.uk/theme/economy>,
                <https://data.ons.gov.uk/theme/prices> ;
            ons:nextRelease "2023-09-20T07:00:00+00:00"^^xsd:dateTime .

        _:b1 dcat:endDate "2023-08-01T00:00:00+00:00"^^xsd:dateTime ;
            dcat:startDate "1989-01-01T00:00:00+00:00"^^xsd:dateTime .

        _:b2 vcard:fn "Consumer Price Inflation Enquiries"@en ;
            vcard:hasEmail <mailto:cpi@ons.gov.uk> .
    }
    """
    db.parse(data=data, format="trig")
    result = crud.get_dataset(db, "cpih")
    assert sort_dict_and_list_keys(result) == sort_dict_and_list_keys(
        dataset_response_metadata
    )
