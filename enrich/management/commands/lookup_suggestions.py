import traceback
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm
from django.core.management.base import BaseCommand

from enrich.lookup import query_suggestion
from enrich.models import Suggestion
from ifx.quirks import patch_dns

MAX_WORKERS = 25


class Command(BaseCommand):
    help = "Lookup pending suggestions"

    def add_arguments(self, parser):
        parser.add_argument('--workers', '-w', type=int, default=MAX_WORKERS)

    def handle(self, workers, *args, **options):
        patch_dns()
        c = Counter()
        qs = Suggestion.objects.filter(status__in=(
            Suggestion.Status.PENDING,
            Suggestion.Status.ERROR,
            Suggestion.Status.FOUND_UNVERIFIED,
            Suggestion.Status.NO_RESULTS,
            Suggestion.Status.MANY_RESULTS,
        ))
        try:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                futs = {ex.submit(query_suggestion, o): o for o in qs}
                print("Submitted....")
                p = tqdm.tqdm(as_completed(futs), total=len(futs))
                for fut in p:
                    o = futs[fut]
                    try:
                        b = fut.result()
                        msg = "ok" if b else "fail"
                        c[msg] += 1
                        p.set_description(msg)
                    except Exception as e:
                        msg = e.__class__.__name__
                        c[msg] += 1
                        tqdm.tqdm.write(traceback.format_exc())

        finally:
            for k, v in c.items():
                print(k, v)
