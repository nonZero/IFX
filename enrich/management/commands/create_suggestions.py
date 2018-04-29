from collections import Counter

import tqdm
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Q

from enrich.lookup import create_suggestion
from enrich.models import Suggestion
from ifx.util import is_hebrew
from movies.models import Movie
from people.models import Person


def create_suggestions(qs, attr):
    c = Counter(created=0)
    qs = qs.exclude(**{attr: None})
    try:
        for m in tqdm.tqdm(qs, desc=qs.model.__name__):
            if not is_hebrew(getattr(m, attr)):
                continue

            o, created = create_suggestion(m)

            c['total'] += 1
            if created:
                c['created'] += 1
    finally:
        for k, v in c.items():
            print(k, v)


class Command(BaseCommand):
    help = "Creates Wikidata Suggestions for all movies with hebrew names"

    def handle(self, *args, **options):
        for model in (Movie, Person):
            done = model.objects.filter(Q(wikidata_id__isnull=False) | Q(
                wikidata_status=model.Status.NOT_APPLICABLE))
            qs = Suggestion.objects.filter(
                status__in=Suggestion.Status.INCOMPLETE,
                content_type=ContentType.objects.get_for_model(model),
                object_id__in=done)
            print(f"Deleting {qs.count()} old {model.__name__} suggestions.")
            qs.delete()

        create_suggestions(Movie.objects.filter(wikidata_id__isnull=True),
                           'title_he')
        create_suggestions(
            Person.objects.exclude(movies=None, wikidata_id__isnull=True),
            'name_he')
