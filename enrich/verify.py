import typing
from collections import defaultdict

from django.db.models import Model
from wikidata.client import Client

from enrich.models import Suggestion
from movies.models import Movie
from people.models import Person


def get_people_in_local_movie(movie):
    d = defaultdict(set)
    for mrp in movie.people.exclude(role__wikidata_id=None):
        d[mrp.role.wikidata_id].add(mrp.person)
    return d


def compare(claim, person):
    if person.wikidata_id and claim.id == person.wikidata_id:
        return True
    if 'en' in claim.label and claim.label['en'] == person.name_en:
        return True
    if 'he' in claim.label and claim.label['he'] == person.name_he:
        return True
    return False


def validate_wikidata_movie_people(wikidata_id, people):
    facts = {}
    cl = Client()
    wiki_movie = cl.get(wikidata_id)
    for role in people:
        if not role:
            continue

        claims = wiki_movie.getlist(cl.get(role))
        if not claims:
            continue

        for person in people[role]:
            for claim in claims:
                if compare(claim, person):
                    facts[person] = claim.id

    return facts


def verify_movie(m: Movie, wikidata_id) -> typing.Dict[Model, str]:
    people_in_movie = get_people_in_local_movie(m)
    facts = validate_wikidata_movie_people(wikidata_id, people_in_movie)
    if facts:
        facts[m] = wikidata_id
    return facts


def verify_person(p: Person, wikidata_id) -> typing.Dict[Model, str]:
    raise NotImplementedError(":-)")


def verify_and_update_movie(m: Movie, wikidata_id):
    facts = verify_movie(m, wikidata_id)
    if facts:
        for item, wiki_id in facts.items():
            item.wikidata_id = wiki_id
            item.save()
        return True

    return False

def verify_suggestion(s: Suggestion):
    m = s.entity
    wikidata_id = s.source_key
    if verify_and_update_movie(m, wikidata_id):
        s.status = Suggestion.Status.VERIFIED
        s.save()
        return True

    return False
