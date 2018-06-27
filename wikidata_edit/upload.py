import json
import requests
from requests_oauthlib import OAuth1
from typing import Dict

from .build import build_movie_entity, build_person_entity

WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"

SUMMARY = "Imported from the Israeli Film Archive catalog"


def get_token(auth):
    r = requests.get(WIKIDATA_API_URL, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
    }, auth=auth)
    r.raise_for_status()
    resp = r.json()
    if 'error' in resp:
        raise Exception(f"Error: {json.dumps(resp, indent=2)}")

    token = resp['query']['tokens']['csrftoken']
    return token


def api_call(auth, action, payload):
    token = get_token(auth)
    data = {
        'action': action,
        'format': 'json',
        'token': token,
        'summary': SUMMARY,
        **payload,
    }
    r = requests.post(WIKIDATA_API_URL, data=data, auth=auth)
    r.raise_for_status()
    resp = r.json()
    if 'error' in resp:
        raise Exception(
            f"API Error in: {json.dumps(resp, indent=2)}\nrequest: {data}")
    return resp


def create_claim(auth: OAuth1, entity, property, value):
    """Upload a new entity to wikipedia"""
    return api_call(auth, 'wbcreateclaim', {
        'entity': entity,
        'snaktype': 'value',
        'property': property,
        'value': json.dumps(value),
    })


# def create_external_id_claim(auth: OAuth1, entity, property, value):
#     """Upload a new entity to wikipedia"""
#     return create_claim(auth, entity, property, 'value', json.dumps({
#         {
#             "value": id,
#             "type": "string"
#         }
#     }))


def upload_entity(auth: OAuth1, entity):
    """Upload a new entity to wikipedia"""
    return api_call(auth, 'wbeditentity', {
        'new': 'item',
        'data': json.dumps(entity),
    })


def upload_movie(auth: OAuth1,
                 labels: Dict[str, str],
                 descs: Dict[str, str],
                 ext_ids: Dict[str, str] = None,
                 year=None,
                 duration=None,
                 aliases=None):
    """A high level interface for adding movies to wikidata"""

    entity = build_movie_entity(descs, duration, ext_ids, labels, year,
                                aliases)
    return upload_entity(auth, entity)


def upload_person(auth: OAuth1,
                  labels: Dict[str, str],
                  descs: Dict[str, str],
                  ext_ids: Dict[str, str] = None,
                  gender: int = None):
    """A high level interface for adding movies to wikidata"""
    entity = build_person_entity(descs, ext_ids, labels, gender)
    return upload_entity(auth, entity)
