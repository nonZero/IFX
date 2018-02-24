from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm
import traceback
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from enrich.models import Suggestion
from enrich.verify import verify_suggestion
from movies.models import Movie

MAX_WORKERS = 25


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
    help = "Verify unverified suggestions"

    def handle(self, *args, **options):
        patch_dns()
        c = Counter()
        qs = Suggestion.objects.filter(
            content_type=ContentType.objects.get_for_model(Movie),
            status=Suggestion.Status.FOUND_UNVERIFIED,
        ).order_by("?")

        try:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
                futs = {ex.submit(verify_suggestion, o): o for o in qs}
                print("Submitted....")
                for fut in tqdm.tqdm(as_completed(futs), total=len(futs)):
                    o = futs[fut]
                    assert isinstance(o, Suggestion)
                    c['total'] += 1
                    try:
                        verified, n_verified = fut.result()
                        c['suggestions verified'] += verified
                        c['entities verified'] += n_verified
                    except IntegrityError as e:
                        o.status = Suggestion.Status.ERROR
                        o.error_message = traceback.format_exc()
                        o.save()
                        c['integrity error'] += 1


        finally:
            for k, v in c.items():
                print(k, v)
