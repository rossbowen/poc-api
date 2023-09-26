"""
rdflib SPARQLUpdateStore doesn't work well.
"""

import os

from rdflib import Dataset, BNode
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore, _node_to_sparql

OXIGRAPH_URL = os.getenv("OXIGRAPH_URL", "http://localhost:7878")


def skolemise(node):
    if isinstance(node, BNode):
        return "<bnode:b%s>" % node
    return _node_to_sparql(node)


configuration = (f"{OXIGRAPH_URL}/query", f"{OXIGRAPH_URL}/update")


db = Dataset(store=SPARQLUpdateStore(*configuration, node_to_sparql=skolemise))
