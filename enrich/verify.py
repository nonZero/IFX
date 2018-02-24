from movies.models import Movie
from people.models import Person


def verify_movie(m: Movie, wikidata_id) -> bool:
    raise NotImplementedError(":-)")


def verify_person(p: Person, wikidata_id) -> bool:
    raise NotImplementedError(":-)")
