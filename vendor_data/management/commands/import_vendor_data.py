from collections import Counter

import argparse
import json
from django.core.management.base import BaseCommand
from django.db import transaction

from vendor_data import models


class Command(BaseCommand):
    help = "Import vendor data from jsonlines"

    def add_arguments(self, parser):
        parser.add_argument('infile', type=argparse.FileType('r'),
                            help='file path to import from')

    def handle(self, infile, *args, **options):
        c = Counter()
        try:
            for i, s in enumerate(infile):
                row = json.loads(s.strip())
                v, created = models.Vendor.objects.get_or_create(
                    key=row['vendor'])
                if created:
                    print(f"Vendor created: {v.key}")
                with transaction.atomic():
                    o, created = v.items.update_or_create(
                        vid=row['id'],
                        defaults=dict(
                            type=models.VendorItem.Type.MOVIE,
                            title_he=row.get('title_he'),
                            title_en=row.get('title_en'),
                            year=row.get('year'),
                            duration=row.get('duration'),
                            summary_he=row.get('summary_he'),
                            imdb_id=row.get('imdb'),
                            editing_comment=row.get('extra'),
                            extra_data={
                                'director': row.get('director'),
                            }
                        ),
                    )
                    msg = 'created' if created else 'updated'
                    c[msg] += 1
                    c[v] += 1
                    c[f"{v}.{msg}"] += 1
                    for t in row.get('tags', []):
                        g, created = v.genre.get_or_create(value=t)
                        if created:
                            c[f'{v}.g_created'] += 1
                        o.genre.add(g)
                        c['tags'] += 1
                        c[f'{v}.tags'] += 1
        finally:
            for k, v in c.most_common():
                print(k, v)
