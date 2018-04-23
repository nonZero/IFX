from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import shuffle

import tqdm
from django.core.management.base import BaseCommand

from enrich.lookup import create_sitelinks
from ifx.quirks import patch_dns
from movies.models import Movie
from people.models import Person
import logging

MAX_WORKERS = 5


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create wikipedia articals links based on WikiData"

    def add_arguments(self, parser):
        parser.add_argument('--workers', '-w', type=int, default=MAX_WORKERS)

    def handle(self, workers, *args, **options):
        patch_dns()
        c = Counter()
        objs = list(Movie.objects.exclude(wikidata_id=None)) + list(
            Person.objects.exclude(wikidata_id=None))
        shuffle(objs)
        try:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                futs = {ex.submit(create_sitelinks, o): o for o in objs}
                for fut in tqdm.tqdm(as_completed(futs), total=len(futs)):
                    o = futs[fut]
                    try:
                        c.update(fut.result())
                    except Exception as e:
                        logger.exception(f"Error while processing {o}: {e}")
                        c[e.__class__.__name__] += 1
        finally:
            for k, v in c.items():
                print(k, v)
