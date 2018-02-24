from collections import defaultdict
from wikidata.client import Client
from movies.models import Movie
from people.models import Person


def get_people_in_local_movie(movie):
    d = defaultdict(set)
    for mrp in movie.people.exclude(role__wikidata_id=None):
        d[mrp.role.wikidata_id].add(mrp.person)
    return d


def validate_wikidata_movie_people(wikidata_id, people):
    cl = Client()
    wiki_movie = cl.get(wikidata_id)
    for role in people:
        if not role:
            continue

        claims = wiki_movie.getlist(cl.get(role))
        if not claims:
            continue

        for person in people[role]:
            for item in claims:
                if person.wikidata_id and item.id == person.wikidata_id:
                    return True
                if 'en' in item.label and item.label['en'] == person.name_en:
                    return True
                if 'he' in item.label and item.label['he'] == person.name_he:
                    return True

    return False


def verify_movie(m: Movie, wikidata_id) -> bool:
    people_in_movie = get_people_in_local_movie(m)
    is_valid = validate_wikidata_movie_people(wikidata_id, people_in_movie)
    return is_valid


def verify_person(p: Person, wikidata_id) -> bool:
    raise NotImplementedError(":-)")
