import pandas as pd
from django.core.exceptions import ObjectDoesNotExist

from django.core.management.base import BaseCommand
from tqdm import tqdm

from movies.models import Movie, Description


class Command(BaseCommand):
    help = "Import description."

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
            if str(row.book_id).isdigit():
                if Movie.objects.filter(bid=row.book_id):
                    o = Description()
                    o.movie = Movie.objects.get(bid=row.book_id)
                    o.summery = row.summary
                    o.lang = row.lang_id
                    if not options['readonly']:
                        o.save()
            progress.update(1)
        progress.close()
