"""This is a quick and (very) dirty solution to match 3rd party sites' data with IFX
data for verification.

It works :-)
"""

from collections import Counter

import difflib
from django.core.management.base import BaseCommand

from links.models import Link
from movies.models import Movie
from vendor_data import models


class Command(BaseCommand):
    help = "Matches vendor and IFX data"

    def handle(self, *args, **options):

        titles = sorted(
            {m.title_he for m in Movie.objects.active().filter(title_he__isnull=False)})

        c = Counter()

        # FIXME: filter by status?
        qs = models.VendorItem.objects.filter(object_id=None)

        print(f"Checking {qs.count()} movies.")

        for o in qs:  # type: models.VendorItem
            l = Link.objects.filter(type__wikidata_id=o.vendor.pid,
                                    value=o.vid).first()
            if l:
                c['bingo-vid!'] += 1
                o.entity = l.entity
                o.status = o.Status.ASSIGNED
                o.save()
                continue

            if o.imdb_id:
                l = Link.objects.filter(type__slug='imdb',
                                        value=o.imdb_id).first()
                if l:
                    c['bingo-imdb!'] += 1
                    o.entity = l.entity
                    o.status = o.Status.ASSIGNED
                    o.save()
                    continue

            mqs = Movie.objects.active().filter(title_he=o.title_he)
            if mqs.count() > 1:
                mqs = Movie.objects.active().filter(title_he=o.title_he, year=o.year)
            if mqs.count() == 0 and o.title_en:
                mqs = Movie.objects.active().filter(title_en=o.title_en)
            if mqs.count() > 1:
                print(o.title_he, mqs.count())
                c['too-many'] += 1
                # TODO
                continue

            if not mqs.count():
                near = difflib.get_close_matches(o.title_he, titles,
                                                 cutoff=0.9)
                if not near:
                    c['miss'] += 1
                    continue

                print(o.title_he)
                w = near[0]
                ratio = difflib.SequenceMatcher(a=o.title_he, b=w).ratio()
                print(f"--> {w} {ratio:0.3f}")
                try:
                    m = Movie.objects.active().get(title_he=w)
                except Movie.MultipleObjectsReturned:
                    try:
                        m = Movie.objects.active().get(title_he=w, year=o.year)
                    except Movie.DoesNotExist:
                        print("***", w)
                        c['miss????'] += 1
                        # TODO
                        continue
            else:
                m = mqs[0]

            if o.year and m.year and abs(o.year - m.year) > 3:
                c['too-far'] += 1
                continue

            if o.year and m.year and abs(o.year - m.year) <= 2:
                if o.duration == m.duration or o.duration is None or m.duration is None or abs(
                        o.duration - m.duration) < o.duration / 5:
                    c['bingo-year-duration'] += 1
                    o.entity = m
                    o.status = o.Status.ASSIGNED
                    o.save()
                    continue

            director = o.extra_data and o.extra_data.get('director')
            if director:
                r = m.people.filter(role__idea_tid="BAMAI",
                                    person__name_he=director)
                if r:
                    o.entity = m
                    o.status = o.Status.ASSIGNED
                    o.save()
                    c['bingo-director'] += 1
                    continue

            print(o.title_he)
            print(o.year, m.year)
            print(o.duration, m.duration)
            print(director, [r.person.name_he for r in
                             m.people.filter(role__idea_tid="BAMAI")])
            c['maybe'] += 1
            print()

        for k, v in sorted(c.items()):
            print(k, v)
