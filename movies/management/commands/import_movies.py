import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from tqdm import tqdm

from movies.models import Movie


class Command(BaseCommand):
    help = "Import movies."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str,
                            help='file path to import from')

        parser.add_argument(
            '--readonly',
            action='store_true',
            dest='readonly',
            help='Parse it without saving to database',
        )

        parser.add_argument(
            '--json',
            action='store_true',
            dest='json',
            help='input is json file',
        )

    def handle(self, f, **options):
        if options['json']:
            return self.handle_json(f, **options)

        df = pd.read_csv(f, delimiter='\t')

        for i, row in tqdm(df.iterrows(), total=len(df)):
            o, created = Movie.objects.get_or_create(idea_bid=row.bid)
            o.year = None if np.isnan(row.year) else row.year
            self.update_title(o, row.title, row.lang)
            o.full_clean()
            if not options['readonly']:
                o.save()

    @staticmethod
    def update_title(movie, title, lang):
        if np.isnan(lang):
            print('Error - language field is NaN')
            return

        if int(lang) == 1:  # HEB
            movie.title_he = title
        elif int(lang) == 2:  # ENG
            movie.title_en = title
        else:
            print(
                'Proper language title not found, lang="{}", title="{}"'.format(
                    lang, title))
