from collections import Counter

import tqdm
from django.core.management.base import BaseCommand

from enrich.lookup import create_suggestion
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
        create_suggestions(Movie.objects.all(), 'title_he')
        create_suggestions(Person.objects.exclude(movies=None), 'name_he')
