from rdflib import Graph

from rdflib import Graph, URIRef, Literal, BNode
from poc_api.queries import (
    construct_dataset_core,
    construct_dataset_themes,
    construct_dataset_keywords,
    construct_dataset_contact_point,
    construct_dataset_temporal_coverage,
)


def test_construct_dataset_core():
    graph = Graph()
    ds_uri = URIRef("http://example.com/dataset")

    # fmt: off
    graph.add((ds_uri, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://www.w3.org/ns/dcat#DatasetSeries")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/identifier"), Literal("123")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/title"), Literal("My Dataset")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/description"), Literal("A description of my dataset")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/abstract"), Literal("A summary of my dataset")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/issued"), Literal("2022-01-01T00:00:00+00:00")))
    graph.add((ds_uri, URIRef("https://data.ons.gov.uk/ns#nextRelease"), Literal("2022-02-01T00:00:00+00:00")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/publisher"), URIRef("http://example.com/publisher")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/creator"), URIRef("http://example.com/creator")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/accrualPeriodicity"), URIRef("http://purl.org/cld/freq/monthly")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/license"), URIRef("http://example.com/license")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/spatial"), URIRef("http://statistics.data.gov.uk/id/statistical-geography/K02000001")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/temporalResolution"), Literal("P1D")))
    # fmt: on

    result = construct_dataset_core(graph)

    assert isinstance(result, Graph)

    assert len(result) == 13

    # fmt: off
    assert (ds_uri, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://www.w3.org/ns/dcat#DatasetSeries")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/identifier"), Literal("123")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/title"), Literal("My Dataset")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/description"), Literal("A description of my dataset")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/abstract"), Literal("A summary of my dataset")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/issued"), Literal("2022-01-01T00:00:00+00:00")) in result
    assert (ds_uri, URIRef("https://data.ons.gov.uk/ns#nextRelease"), Literal("2022-02-01T00:00:00+00:00")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/publisher"), URIRef("http://example.com/publisher")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/creator"), URIRef("http://example.com/creator")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/accrualPeriodicity"), URIRef("http://purl.org/cld/freq/monthly")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/license"), URIRef("http://example.com/license")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/spatial"), URIRef("http://statistics.data.gov.uk/id/statistical-geography/K02000001")) in result
    assert (ds_uri, URIRef("http://purl.org/dc/terms/temporalResolution"), Literal("P1D")) in result
    # fmt: on


def test_construct_dataset_themes():
    graph = Graph()
    ds_uri = URIRef("http://example.com/dataset")
    theme_uri = URIRef("http://example.com/theme")
    graph.add(
        (
            ds_uri,
            URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            URIRef("http://www.w3.org/ns/dcat#DatasetSeries"),
        )
    )
    graph.add((ds_uri, URIRef("http://www.w3.org/ns/dcat#theme"), theme_uri))

    result = construct_dataset_themes(graph)

    assert isinstance(result, Graph)

    assert (ds_uri, URIRef("http://www.w3.org/ns/dcat#theme"), theme_uri) in result


def test_construct_dataset_keywords():
    graph = Graph()
    ds_uri = URIRef("http://example.com/dataset")
    graph.add(
        (
            ds_uri,
            URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            URIRef("http://www.w3.org/ns/dcat#DatasetSeries"),
        )
    )
    graph.add((ds_uri, URIRef("http://www.w3.org/ns/dcat#keyword"), Literal("keyword")))

    result = construct_dataset_keywords(graph)

    assert isinstance(result, Graph)

    assert (
        ds_uri,
        URIRef("http://www.w3.org/ns/dcat#keyword"),
        Literal("keyword"),
    ) in result


def test_construct_dataset_contact_point():
    graph = Graph()
    ds_uri = URIRef("http://example.com/dataset")
    contact_point = BNode()

    # fmt: off
    graph.add((ds_uri, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://www.w3.org/ns/dcat#DatasetSeries")))
    graph.add((ds_uri, URIRef("http://www.w3.org/ns/dcat#contactPoint"), contact_point))
    graph.add((contact_point, URIRef("http://www.w3.org/2006/vcard/ns#fn"), Literal("John Smith")))
    graph.add((contact_point, URIRef("http://www.w3.org/2006/vcard/ns#hasEmail"), URIRef("mailto:john@example.com")))
    # fmt: on

    result = construct_dataset_contact_point(graph)

    assert isinstance(result, Graph)

    # fmt: off
    assert (ds_uri, URIRef("http://www.w3.org/ns/dcat#contactPoint"), contact_point) in result
    assert (contact_point, URIRef("http://www.w3.org/2006/vcard/ns#fn"), Literal("John Smith")) in result
    assert (contact_point, URIRef("http://www.w3.org/2006/vcard/ns#hasEmail"), URIRef("mailto:john@example.com")) in result
    # fmt: on


def test_construct_dataset_temporal_coverage():
    graph = Graph()
    ds_uri = URIRef("http://example.com/dataset")
    temporal_coverage = BNode()

    # fmt: off
    graph.add((ds_uri, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://www.w3.org/ns/dcat#DatasetSeries")))
    graph.add((ds_uri, URIRef("http://purl.org/dc/terms/temporal"), temporal_coverage))
    graph.add((temporal_coverage, URIRef("http://www.w3.org/ns/dcat#startDate"), Literal("2022-01-01T00:00:00+00:00")))
    graph.add((temporal_coverage, URIRef("http://www.w3.org/ns/dcat#endDate"), Literal("2022-12-31T00:00:00+00:00")))
    # fmt: on

    result = construct_dataset_temporal_coverage(graph)

    assert isinstance(result, Graph)

    # fmt: off
    assert (ds_uri, URIRef("http://purl.org/dc/terms/temporal"), temporal_coverage) in result
    assert (temporal_coverage, URIRef("http://www.w3.org/ns/dcat#startDate"), Literal("2022-01-01T00:00:00+00:00")) in result
    assert (temporal_coverage, URIRef("http://www.w3.org/ns/dcat#endDate"), Literal("2022-12-31T00:00:00+00:00")) in result
    # fmt: on
