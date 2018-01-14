import pandas as pd
import numpy as np
from tqdm import tqdm

from django.core.management.base import BaseCommand

from movies.models import Tag


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
        df = pd.read_csv(f, delimiter='\t')

        progress = tqdm(total=len(df))

        for i, row in df.iterrows():
            tag, created = Tag.objects.get_or_create(tid=row.book_id_s)
            if created:
                tag.tid = row.book_id_s
            tag.title = row.title
            tag.type_id = row.type1_id
            self.update_lang(tag, row.lang_id)
            if not options['readonly']:
                tag.save()
            progress.update(1)

        progress.close()

    @staticmethod
    def update_lang(tag, lang):
        if pd.isnull(lang):
            print('Error - language tag is NaN')
            return

        if str(lang) == 'HEB' or \
                (lang.isdigit() and int(lang) == 1):  # HEB
            tag.lang = 'he'
        elif str(lang) == 'ENG' or \
                (lang.isdigit() and int(lang) == 1):  # ENG
            tag.lang = 'en'
        else:
            print('Proper language not found, lang="{}"'.format(lang))
