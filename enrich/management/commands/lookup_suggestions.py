from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm
from django.core.management.base import BaseCommand

from enrich.lookup import query_suggestion
from enrich.models import Suggestion

MAX_WORKERS = 50


class Command(BaseCommand):
    help = "Lookup pending suggestions"

    def handle(self, *args, **options):
        c = Counter()
        qs = Suggestion.objects.filter(status=Suggestion.Status.PENDING)
        try:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
                futs = {ex.submit(query_suggestion, o): o for o in qs}
                print("Submitted....")
                for fut in tqdm.tqdm(as_completed(futs), total=len(futs)):
                    o = futs[fut]
                    b = fut.result()
                    c["ok" if b else "fail"] += 1
        finally:
            for k, v in c.items():
                print(k, v)
