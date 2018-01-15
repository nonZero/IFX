from collections import Counter
from pprint import pprint

import pandas as pd
from django.core.management.base import BaseCommand
from tqdm import tqdm

from movies.models import models, Movie


class Command(BaseCommand):
    help = "Import movie titles translations."

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
        c = Counter()
        try:
            df = pd.read_csv(f, delimiter='\t')
            progress = tqdm(total=len(df))
            for i, row in df.iterrows():
                try:
                    if str(row.book_id).isdigit():
                        m = Movie.objects.get(bid=row.book_id)
                        if row.lang_id == "ENG":
                            m.title_en = row.title
                        elif row.lang_id == "HEB":
                            m.title_he = row.title
                        else:
                            assert False, row
                        c[row.lang_id] += 1
                except models.ObjectDoesNotExist:
                    # log error to server?
                    c['missing'] += 1
                finally:
                    progress.update(1)
            progress.close()
        finally:
            pprint(c.most_common())
