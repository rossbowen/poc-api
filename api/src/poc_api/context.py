"""
Note that the use of the `@version` keyword under the `publisher` key is a
workaround for a problem in pyld's expansion algorithm.
"""

CONTEXT = {
    "dcat": "http://www.w3.org/ns/dcat#",
    "dcterms": "http://purl.org/dc/terms/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "ons": "https://data.ons.gov.uk/ns#",
    "vcard": "http://www.w3.org/2006/vcard/ns#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "creator": {
        "@id": "dcterms:creator",
        "@type": "@id",
        "@context": {
            "@base": "https://www.gov.uk/government/organisations/",
        },
    },
    "contact_point": {
        "@id": "dcat:contactPoint",
        "@type": "@id",
        "@context": {
            "email": {
                "@id": "vcard:hasEmail",
                "@type": "@id",
            },
            "name": {
                "@id": "vcard:fn",
                "@language": "en",
            },
        },
    },
    "description": {
        "@id": "dcterms:description",
        "@language": "en",
    },
    "distribution": {
        "@id": "dcat:distribution",
        "@type": "@id",
    },
    "frequency": {
        "@id": "dcterms:accrualPeriodicity",
        "@type": "@id",
        "@context": {
            "@base": "http://purl.org/cld/freq/",
        },
    },
    "identifier": {
        "@id": "dcterms:identifier",
    },
    "in_series": {
        "@id": "dcat:inSeries",
        "@type": "@id",
    },
    "issued_date": {
        "@id": "dcterms:issued",
        "@type": "xsd:dateTime",
    },
    "keywords": {
        "@id": "dcat:keyword",
        "@language": "en",
    },
    "landing_page": {
        "@id": "dcat:landingPage",
        "@type": "@id",
    },
    "licence": {
        "@id": "dcterms:license",
        "@type": "@id",
    },
    "next_release_date": {
        "@id": "ons:nextRelease",
        "@type": "xsd:dateTime",
    },
    "publisher": {
        "@id": "dcterms:publisher",
        "@type": "@id",
        "@context": {
            "@base": "https://www.gov.uk/government/organisations/",
            "@version": 1.1,
        },
    },
    "spatial_coverage": {
        "@id": "dcterms:spatial",
        "@type": "@id",
        "@context": {
            "@base": "http://statistics.data.gov.uk/id/statistical-geography/",
        },
    },
    "summary": {
        "@id": "dcterms:abstract",
        "@language": "en",
    },
    "temporal_coverage": {
        "@id": "dcterms:temporal",
        "@type": "@id",
        "@context": {
            "end": {
                "@id": "dcat:endDate",
                "@type": "xsd:dateTime",
            },
            "start": {
                "@id": "dcat:startDate",
                "@type": "xsd:dateTime",
            },
        },
    },
    "temporal_resolution": {
        "@id": "dcterms:temporalResolution",
        "@type": "xsd:duration",
    },
    "theme": {
        "@id": "dcat:theme",
        "@type": "@id",
        "@context": {
            "@base": "https://data.ons.gov.uk/theme/",
        },
    },
    "title": {
        "@id": "dcterms:title",
        "@language": "en",
    },
}


def replace_context_with_local(data: dict) -> dict:
    if not isinstance(data, dict):
        raise TypeError("data must be a dict")
    data = data.copy()
    if "@context" not in data:
        raise ValueError("data does not contain a @context")
    data["@context"] = CONTEXT
    return data


def replace_context_with_remote(data: dict) -> dict:
    if not isinstance(data, dict):
        raise TypeError("data must be a dict")
    data = data.copy()
    data["@context"] = "https://data.ons.gov.uk/ns#"
    return data
