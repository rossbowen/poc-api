import string

from rdflib import Graph


def construct_catalogue_record(dataset_iri: str, catalog_record_iri: str) -> str:
    query = string.Template(
        """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        INSERT {
            <https://data.ons.gov.uk/datasets> dcat:record ?record .

            ?record a dcat:CatalogRecord ;
                foaf:primaryTopic ?ds .
        }
        WHERE {
            VALUES ?ds { <${dataset_iri}> }
            VALUES ?record { <${catalog_record_iri}> }
        }
        """
    ).substitute(dataset_iri=dataset_iri, catalog_record_iri=catalog_record_iri)
    return query


def construct_dataset_core(graph: Graph) -> Graph:
    query = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX ons: <https://data.ons.gov.uk/ns#>
        CONSTRUCT WHERE {
            ?ds a dcat:DatasetSeries ;
                dcterms:identifier ?identifier ;
                dcterms:title ?title ;
                dcterms:description ?description ;
                dcterms:abstract ?summary ;
                dcterms:issued ?release_date ;
                ons:nextRelease ?next_release ;
                dcterms:publisher ?publisher ;
                dcterms:creator ?creator ;
                dcterms:accrualPeriodicity ?frequency ;
                dcterms:license ?license ;
                dcterms:spatial ?spatial_coverage ;
                dcterms:temporalResolution ?temporal_resolution .
        }
        """
    results_graph = graph.query(query).graph
    result = results_graph if results_graph else Graph()
    return result


def construct_dataset_themes(graph: Graph) -> Graph:
    query = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        CONSTRUCT WHERE {
            ?ds a dcat:DatasetSeries ;
                dcat:theme ?theme .
        }
        """
    results_graph = graph.query(query).graph
    result = results_graph if results_graph else Graph()
    return result


def construct_dataset_keywords(graph: Graph) -> Graph:
    query = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        CONSTRUCT WHERE {
            ?ds a dcat:DatasetSeries ;
                dcat:keyword ?keyword .
        }
        """
    results_graph = graph.query(query).graph
    result = results_graph if results_graph else Graph()
    return result


def construct_dataset_contact_point(graph: Graph) -> Graph:
    query = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        CONSTRUCT WHERE {
            ?ds a dcat:DatasetSeries ;
                dcat:contactPoint ?contact_point .

            ?contact_point vcard:fn ?name ;
                vcard:hasEmail ?email .
        }
        """
    results_graph = graph.query(query).graph
    result = results_graph if results_graph else Graph()
    return result


def construct_dataset_temporal_coverage(graph: Graph) -> Graph:
    query = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        CONSTRUCT WHERE {
            ?ds a dcat:DatasetSeries ;
                dcterms:temporal ?temporal_coverage .

            ?temporal_coverage dcat:startDate ?start_date ;
                dcat:endDate ?end_date .
        }
        """
    results_graph = graph.query(query).graph
    result = results_graph if results_graph else Graph()
    return result


def construct_edition_core(graph: Graph) -> Graph:
    query = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        CONSTRUCT WHERE {
            ?ds a dcat:Dataset ;
                dcterms:identifier ?identifier ;
                dcat:inSeries ?series ;
                dcterms:title ?title ;
                dcterms:description ?description ;
                dcterms:abstract ?summary ;
                dcterms:issued ?release_date ;
                dcterms:license ?license .
        }
        """
    results_graph = graph.query(query).graph
    result = results_graph if results_graph else Graph()
    return result


def construct_edition_distribution(graph: Graph) -> Graph:
    query = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        CONSTRUCT WHERE {
            ?ds a dcat:Dataset ;
                dcat:distribution ?distribution .
        }
        """
    results_graph = graph.query(query).graph
    result = results_graph if results_graph else Graph()
    return result
