from celery import shared_task

from enrich.lookup import create_missing_links
from links.consts import ENTITY_MODELS, ENTITY_MODELS_REVERSE
from movies.models import Movie
from people.models import Person


def add_links(entity):
    entity_type = ENTITY_MODELS_REVERSE[entity.__class__]
    return add_links_by_id.delay(entity_type, entity.id)


@shared_task
def add_links_by_id(entity_type, id):
    model = ENTITY_MODELS[entity_type]
    o = model.objects.get(id=id)
    return create_missing_links(o)


@shared_task
def add_links_by_movie_id(id):
    o = Movie.objects.get(id=id)
    return create_missing_links(o)


@shared_task
def add_links_by_person_id(id):
    o = Person.objects.get(id=id)
    return create_missing_links(o)
