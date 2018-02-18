import math
from collections import Counter

import pandas as pd
from django.core.management.base import BaseCommand
from tqdm import tqdm

from movies.models import Movie


class Command(BaseCommand):
    help = "Import tags."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str,
                            help='file path to import from')

        parser.add_argument(
            '--readonly',
            action='store_true',
            dest='readonly',
            help='Parse it without saving to database',
        )

    def handle(self, f, **options):
        # flds = {f.fid: f.title for f in Field.objects.all()}
        df = pd.read_csv(f, delimiter='\t')
        c = Counter()
        try:
            for i, row in tqdm(df.iterrows(), total=len(df)):
                if row.lif != "#46":
                    c["unknown"] += 1
                    continue
                if not row.book_id.isnumeric():
                    # print(row.book_id, row.lif, flds[row.lif], row.string1_id)
                    c["bad id"] += 1
                    continue

                try:
                    m = Movie.objects.get(bid=row.book_id)
                    v = row.string1_id.strip()
                    if " " in v and v.split()[1].startswith('ד'):
                        v = v.split()[0]
                    elif "." in v:
                        try:
                            v = str(math.ceil(float(v)))
                        except ValueError:
                            pass
                    elif ":" in v:
                        v = str(math.ceil(float(v.split(":")[0])))

                    if not v.isnumeric():
                        print("BAD", m.id, m, row.book_id, v)
                        c['bad value'] += 1
                        continue
                    n = int(v)
                    if m.duration != n:
                        m.duration = n
                        m.save()
                        c['updated'] += 1
                    else:
                        c['ok'] += 1
                except Movie.DoesNotExist:
                    # print("No movie", row.book_id)
                    c['*missing'] += 1
        finally:
            for k, v in sorted(c.items()):
                print(k, v)
