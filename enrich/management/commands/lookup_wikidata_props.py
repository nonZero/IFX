from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import shuffle

import tqdm
from django.core.management.base import BaseCommand

from enrich.lookup import create_missing_links
from movies.models import Movie
from people.models import Person

MAX_WORKERS = 20

import logging

logger = logging.getLogger(__name__)


def patch_dns():
    import socket
    prv_getaddrinfo = socket.getaddrinfo
    dns_cache = {}  # or a weakref.WeakValueDictionary()

    def new_getaddrinfo(*args):
        try:
            return dns_cache[args]
        except KeyError:
            res = prv_getaddrinfo(*args)
            dns_cache[args] = res
            return res

    socket.getaddrinfo = new_getaddrinfo


class Command(BaseCommand):
    help = "Create links based on WikiData"

    def handle(self, *args, **options):
        patch_dns()
        c = Counter()
        objs = list(Movie.objects.exclude(wikidata_id=None)) + list(
            Person.objects.exclude(wikidata_id=None))
        shuffle(objs)
        try:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
                futs = {ex.submit(create_missing_links, o): o for o in objs}
                print("Submitted....")
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
