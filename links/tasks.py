from celery import shared_task

from enrich.lookup import create_missing_links
from movies.models import Movie
from people.models import Person


@shared_task
def add_links_by_movie_id(id):
    o = Movie.objects.get(id=id)
    return create_missing_links(o)


@shared_task
def add_links_by_person_id(id):
    o = Person.objects.get(id=id)
    return create_missing_links(o)
