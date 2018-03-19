import traceback
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from enrich.models import Suggestion
from enrich.verify import verify_suggestion
from ifx.quirks import patch_dns

MAX_WORKERS = 25


class Command(BaseCommand):
    help = "Verify unverified suggestions"

    def add_arguments(self, parser):
        parser.add_argument('--workers', '-w', type=int, default=MAX_WORKERS)

    def handle(self, workers, *args, **options):
        patch_dns()
        c = Counter()
        qs = Suggestion.objects.filter(
            status=Suggestion.Status.FOUND_UNVERIFIED,
        ).order_by("?")

        try:
            with ThreadPoolExecutor(max_workers=workers) as ex:
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
                    except Exception as e:
                        msg = e.__class__.__name__
                        c[msg] += 1
                        tqdm.tqdm.write(traceback.format_exc())


        finally:
            for k, v in c.items():
                print(k, v)
