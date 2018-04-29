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
            done = model.objects.filter(
                Q(wikidata_id__isnull=False) |
                Q(wikidata_status=model.Status.NOT_APPLICABLE) |
                Q(active=False))
            qs = Suggestion.objects.filter(
                status__in=Suggestion.Status.INCOMPLETE,
                content_type=ContentType.objects.get_for_model(model),
                object_id__in=done)
            print(f"Deleting {qs.count()} old {model.__name__} suggestions.")
            qs.delete()

        qs = Movie.objects.filter(active=True,
                                  wikidata_id__isnull=True)
        create_suggestions(qs, 'title_he')

        qs = Person.objects.filter(
            active=True, wikidata_id__isnull=True).exclude(movies=None)
        create_suggestions(qs, 'name_he')
