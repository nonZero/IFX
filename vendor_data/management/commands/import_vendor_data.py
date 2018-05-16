from collections import Counter

import argparse
import json
from django.core.management.base import BaseCommand
from django.db import transaction

from vendor_data import models


class Command(BaseCommand):
    help = "Import vendor data from json"

    def add_arguments(self, parser):
        parser.add_argument('pid')
        parser.add_argument('infile', type=argparse.FileType('r'),
                            help='file path to import from')

    def handle(self, pid, infile, *args, **options):
        v = models.Vendor.objects.get(pid=pid)
        data = json.load(infile)
        c = Counter()
        with transaction.atomic():
            for row in data:
                o, created = v.items.update_or_create(
                    vid=row['id'],
                    defaults=dict(
                        type=models.VendorItem.Type.MOVIE,
                        title_he=row['title_he'],
                        title_en=row.get('title_en'),
                        year=row['year'],
                        duration=row.get('duration'),
                        summary_he=row['summary_he'],
                        imdb_id=row.get('imdb'),
                        editing_comment=row.get('extra'),
                        extra_data={
                            'director': row.get('director'),
                        }
                    ),
                )
                c['created' if created else 'updated'] += 1
                for t in row.get('tags', []):
                    g, created = v.genre.get_or_create(value=t)
                    if created:
                        c['g_created'] += 1
                    o.genre.add(g)
                    c['tags'] += 1
        for k, v in sorted(c.items()):
            print(k, v)