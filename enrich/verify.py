from collections import defaultdict
from typing import Dict, Set

from django.db import transaction
from django.db.models import Model
from wikidata.client import Client
from wikidata.entity import Entity

from enrich.models import Suggestion, Source
from movies.models import Movie
from people.models import Person


def get_people_by_pid(movie) -> Dict[str, Set[Person]]:
    d = defaultdict(set)
    for mrp in movie.people.exclude(role__wikidata_id=None):
        d[mrp.role.wikidata_id].add(mrp.person)
    return d


def is_same_person(claim: Entity, person: Person):
    if person.wikidata_id and claim.id == person.wikidata_id:
        return True
    if 'en' in claim.label and claim.label['en'] == person.name_en:
        return True
    if 'he' in claim.label and claim.label['he'] == person.name_he:
        return True
    return False


def validate_wikidata_movie_people(wikidata_id, people_by_pid):
    cl = Client()
    wiki_movie = cl.get(wikidata_id)

    facts = {}
    for role, people in people_by_pid.items():
        wiki_people = wiki_movie.getlist(cl.get(role))

        for person in people:
            for wiki_person in wiki_people:
                if is_same_person(wiki_person, person):
                    facts[person] = wiki_person.id

    return facts


def verify_movie(m: Movie, wikidata_id) -> Dict[Model, str]:
    people_in_movie = get_people_by_pid(m)
    facts = validate_wikidata_movie_people(wikidata_id, people_in_movie)
    if facts:
        facts[m] = wikidata_id
    return facts


def verify_person(p: Person, wikidata_id) -> Dict[Model, str]:
    raise NotImplementedError(":-)")


def verify_and_update_movie(m: Movie, wikidata_id):
    n = 0
    facts = verify_movie(m, wikidata_id)
    for item, wiki_id in facts.items():
        if item.wikidata_id != wiki_id:
            item.wikidata_status = Movie.Status.ASSIGNED
            item.wikidata_id = wiki_id
            item.save()
            n += 1

    return n, facts


def verify_suggestion(s: Suggestion):
    assert s.source == Source.WIKIDATA
    assert s.status == s.Status.FOUND_UNVERIFIED
    assert isinstance(s.entity, Movie)  # TODO: Person

    with transaction.atomic():
        n, facts = verify_and_update_movie(s.entity, s.source_key)
        if s.entity in facts:
            s.status = Suggestion.Status.VERIFIED
            s.save()
            return True, n

    return False, n
