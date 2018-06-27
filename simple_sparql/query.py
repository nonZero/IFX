import requests


def simple_query(query):
    r = requests.get("https://query.wikidata.org/sparql", {
        'query': query,
        'format': 'json',
    })
    r.raise_for_status()
    return r.json()['results']['bindings']