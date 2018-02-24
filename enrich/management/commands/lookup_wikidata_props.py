from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm
from django.core.management.base import BaseCommand

from enrich.lookup import get_missing_links
from movies.models import Movie
from people.models import Person

MAX_WORKERS = 50


class Command(BaseCommand):
    help = "Create links based on WikiData"

    def handle(self, *args, **options):
        c = Counter()
        # objs = Movie.objects.exclude(wikidata_id=None)
        objs = list(Movie.objects.exclude(wikidata_id=None)) + list(
            Person.objects.exclude(wikidata_id=None))
        try:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
                futs = {ex.submit(get_missing_links, o): o for o in objs}
                print("Submitted....")
                for fut in tqdm.tqdm(as_completed(futs), total=len(futs)):
                    # o = futs[fut]
                    n = fut.result()
                    c['total'] += 1
                    c['new'] += n
        finally:
            for k, v in c.items():
                print(k, v)
