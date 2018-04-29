import json
from typing import Dict

import requests
from requests_oauthlib import OAuth1

from .build import build_movie_entity, build_person_entity

WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"


def upload_entity(auth: OAuth1, entity):
    """Upload a new entity to wikipedia"""

    summary = "Imported from the Israeli Film Archive catalog"
    r = requests.get(WIKIDATA_API_URL, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
    }, auth=auth)
    r.raise_for_status()
    token = r.json()['query']['tokens']['csrftoken']
    r = requests.post(WIKIDATA_API_URL, data={
        'token': token,
        'format': 'json',
        'action': 'wbeditentity',
        'summary': str(summary),
        'new': 'item',
        'data': json.dumps(entity),
    }, auth=auth)
    r.raise_for_status()
    return r.json()


def upload_movie(auth: OAuth1,
                 labels: Dict[str, str],
                 descs: Dict[str, str],
                 ext_ids: Dict[str, str] = None,
                 year=None,
                 duration=None):
    """A high level interface for adding movies to wikidata"""

    entity = build_movie_entity(descs, duration, ext_ids, labels, year)
    return upload_entity(auth, entity)


def upload_person(auth: OAuth1,
                  labels: Dict[str, str],
                  descs: Dict[str, str],
                  ext_ids: Dict[str, str] = None,
                  gender: int = None):
    """A high level interface for adding movies to wikidata"""
    entity = build_person_entity(descs, ext_ids, labels, gender)
    return upload_entity(auth, entity)
