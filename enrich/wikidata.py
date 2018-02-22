import requests
from wikidata.client import Client


def get_suggestions(query, lang='en'):
    url = "http://www.wikidata.org/w/api.php"
    params = {
        "search": query,
        "action": "wbsearchentities",
        "format": "json",
        "language": lang,
        "limit": "10"
    }
    return requests.get(url, params=params).json()


class TooManyResults(Exception):
    def __init__(self, results, *args):
        self.results = results
        msg = "Too many results: {}".format(", ".join(en.id for en in results))
        super().__init__(msg, *args)


class NoResults(Exception):
    pass


def get_wikidata_result(query):
    cl = Client()
    instance_of = cl.get('P31')
    film = cl.get('Q11424')
    results = get_suggestions(query)
    entities = [cl.get(result['id']) for result in results['search']]
    films = [en for en in entities if
             instance_of in en and en[instance_of] == film]

    if len(films) == 0:
        raise NoResults()

    if len(films) > 1:
        raise TooManyResults(films)

    return films[0]
