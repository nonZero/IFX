import tqdm
from django.core.management.base import BaseCommand

from enrich.lookup import create_suggestion
from ifx.util import is_hebrew
from movies.models import Movie


class Command(BaseCommand):
    help = "Creates Wikidata Suggestions for all movies with hebrew names"

    def handle(self, *args, **options):
        n = 0
        for m in tqdm.tqdm(Movie.objects.exclude(title_he=None)):
            if not is_hebrew(m.title_he):
                continue

            create_suggestion(m)

            n += 1
        print(n)
