import typing

import requests
from wikidata.client import Client

INSTANCE_OF = 'P31'
HUMAN = 'Q5'
FILM = 'Q11424'


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


def get_wikidata_result(query, classifier_pid):
    cl = Client()

    prop = cl.get(INSTANCE_OF)
    q = cl.get(classifier_pid)

    results = get_suggestions(query)

    entities = [cl.get(result['id']) for result in results['search']]
    filtered = [en for en in entities if prop in en and en[prop] == q]

    if len(filtered) == 0:
        raise NoResults()

    if len(filtered) > 1:
        raise TooManyResults(filtered)

    return filtered[0]


def get_props(qid: str, pids: list) -> typing.Dict[str, str]:
    cl = Client()
    entity = cl.get(qid)

    d = dict()

    for pid in pids:
        prop = cl.get(pid)
        if prop in entity:
            d[pid] = entity[prop]

    return d
