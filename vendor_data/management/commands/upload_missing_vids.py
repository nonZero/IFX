import time
from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import Count

from movies.models import Movie
from users.models import User
from wikidata_edit.upload import create_claim


class BetterCounter(Counter):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("----")
        for k, v in self.most_common():
            print("*", k, v)


class Command(BaseCommand):
    help = "Upload to wikidata links to vendors"

    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, email, *args, **options):
        u = User.objects.get(email=email)
        oauth1 = u.get_wikidata_oauth1()

        qs = Movie.objects.exclude(wikidata_id=None).annotate(
            x=Count('vendor_items')
        ).filter(
            x__gt=0,
            vendor_items__wikidata_id__isnull=True
        )

        total = qs.count()
        print(f"checking {total} items")
        with BetterCounter() as c:
            for i, o in enumerate(qs):  # type: (int, Movie)
                print(
                    f"{i + 1}/{total}, #{o.id}={o.wikidata_id}: {o.title_he}")

                for vi in o.vendor_items.filter(wikidata_id=None):
                    print("+", vi.vendor.pid, vi.vid)
                    resp = create_claim(oauth1, o.wikidata_id, vi.vendor.pid,
                                        vi.vid)
                    if resp.get('success') != 1:
                        assert False, resp
                    vi.wikidata_id = o.wikidata_id
                    vi.save()
                    c['added'] += 1
                    c[vi.vendor] += 1

                time.sleep(0.2)
