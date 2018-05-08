from typing import List, Dict

import collections

DURATION = "P2047"
PUBLICATION_DATE = "P577"
INSTANCE_OF = "P31"
FILM = 11424
HUMAN = 5

GENDER = "P21"


def build_claims(claims: List[dict]) -> Dict[str, List[dict]]:
    d = collections.defaultdict(list)
    for c in claims:
        d[c["mainsnak"]["property"]].append(c)
    return d


def create_claim(prop, data_type, data_value):
    return {
        "mainsnak": {
            "snaktype": "value",
            "property": prop,
            "datatype": data_type,
            "datavalue": data_value,
        },
        "type": "statement",
    }


def create_external_id_claim(prop, id):
    return create_claim(prop, "external-id", {
        "value": id,
        "type": "string"
    })


def create_item_claim(prop, id: int):
    return create_claim(prop, "wikibase-item", {
        "value": {
            "entity-type": "item",
            "numeric-id": id,
            "id": f"Q{id}"
        },
        "type": "wikibase-entityid"
    })


def create_instance_of_claim(item_type: int):
    return create_item_claim(INSTANCE_OF, item_type)


def create_year_claim(year):
    s = f"+{year}-00-00T00:00:00Z"
    return create_claim(PUBLICATION_DATE, "time", {
        "value": {
            "time": s,
            "timezone": 0,
            "before": 0,
            "after": 0,
            "precision": 9,
            "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
        },
        "type": "time"
    })


def create_duration_claim(duration: int):
    s = f"+{duration}"
    return create_claim(DURATION, "quantity", {
        "value": {
            "amount": s,
            "unit": "http://www.wikidata.org/entity/Q7727"
        },
        "type": "quantity"
    })


def build_entity(claims, descs, ext_ids, labels, aliases=None):
    if ext_ids:
        for k, v in ext_ids.items():
            claims.append(create_external_id_claim(k, v))
    data = {
        'labels': {k: {'language': k, 'value': v} for k, v in
                   labels.items()},
        'descriptions': {k: {'language': k, 'value': v} for k, v in
                         descs.items()},
        'claims': build_claims(claims),
    }
    if aliases:
        data['aliases'] = {lang: {'language': lang, 'value': v} for lang, v in
                           aliases}
    return data


def build_movie_entity(descs, duration, ext_ids, labels, year, aliases=None):
    claims = [create_instance_of_claim(FILM)]

    if year:
        claims.append(create_year_claim(year))
    if duration:
        claims.append(create_duration_claim(duration))

    return build_entity(claims, descs, ext_ids, labels, aliases)


def build_person_entity(descs, ext_ids, labels, gender):
    claims = [create_instance_of_claim(HUMAN)]
    if gender:
        claims.append(create_item_claim(GENDER, gender))

    return build_entity(claims, descs, ext_ids, labels)
