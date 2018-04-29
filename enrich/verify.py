from collections import defaultdict
from typing import Dict, Set

from django.db import transaction
from django.db.models import Model
from wikidata.client import Client
from wikidata.entity import Entity

from editing_logs.api import Recorder
from enrich.lookup import get_movies_for_person, SparqlMovie
from enrich.models import Suggestion, Source
from enrich.types import IFXEntity
from movies.models import Movie
from people.models import Person


def get_people_by_pid(movie) -> Dict[str, Set[Person]]:
    d = defaultdict(set)
    for mrp in movie.people.exclude(role__wikidata_id=None):
        d[mrp.role.wikidata_id].add(mrp.person)
    return d


def get_movies_by_pid(person) -> Dict[str, Set[Movie]]:
    d = defaultdict(set)
    for mrp in person.movies.exclude(role__wikidata_id=None):
        d[mrp.role.wikidata_id].add(mrp.movie)
    return d


def is_same_person(claim: Entity, person: Person):
    if person.wikidata_id and claim.id == person.wikidata_id:
        return True
    if 'en' in claim.label and claim.label['en'] == person.name_en:
        return True
    if 'he' in claim.label and claim.label['he'] == person.name_he:
        return True
    return False


def is_same_movie(claim: SparqlMovie, movie: Movie):
    if movie.wikidata_id and claim.id == movie.wikidata_id:
        return True
    if claim.en and claim.en == movie.title_en:
        return True
    if claim.he and claim.he == movie.title_he:
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


def validate_wikidata_person_movies(wikidata_id, movies_by_pid):
    wikidata_movies = list(get_movies_for_person(wikidata_id))
    wikidata_movies_per_rel = defaultdict(list)
    for o in wikidata_movies:
        wikidata_movies_per_rel[o.rel].append(o)

    facts = {}
    for role, movies in movies_by_pid.items():
        wiki_movies = wikidata_movies_per_rel.get(role, [])
        for movie in movies:
            for wiki_movie in wiki_movies:
                if is_same_movie(wiki_movie, movie):
                    facts[movie] = wiki_movie.id

    return facts


def verify_movie(m: Movie, wikidata_id) -> Dict[Model, str]:
    people_in_movie = get_people_by_pid(m)
    facts = validate_wikidata_movie_people(wikidata_id, people_in_movie)
    if facts:
        facts[m] = wikidata_id
    return facts


def verify_person(p: Person, wikidata_id) -> Dict[Model, str]:
    movies_for_person = get_movies_by_pid(p)
    facts = validate_wikidata_person_movies(wikidata_id, movies_for_person)
    if facts:
        facts[p] = wikidata_id
    return facts


def verify_and_update_entity(e: IFXEntity, wikidata_id):
    if isinstance(e, Movie):
        facts = verify_movie(e, wikidata_id)
    elif isinstance(e, Person):
        facts = verify_person(e, wikidata_id)
    else:
        raise ValueError(
            f"Must be Person or Movie, got: {e.__class__.__name__}")

    n = 0
    for item, wiki_id in facts.items():
        if item.wikidata_id != wiki_id:
            note = f"Auto verified {item.__class__.__name__} #{item.id} => {wiki_id}"
            with Recorder(note=note) as r:
                r.record_update_before(item)
                item.wikidata_status = Movie.Status.ASSIGNED
                item.wikidata_id = wiki_id
                r.record_update_after(item)
                item.save()
            n += 1

    return n, facts


def verify_suggestion(s: Suggestion):
    assert s.source == Source.WIKIDATA
    assert s.status == s.Status.FOUND_UNVERIFIED

    with transaction.atomic():
        if not s.entity.active:
            return False, 0
        if s.entity.wikidata_id is not None:
            return False, 0
        n, facts = verify_and_update_entity(s.entity, s.source_key)
        if s.entity in facts:
            s.status = Suggestion.Status.VERIFIED
            s.save()
            return True, n

    return False, n
