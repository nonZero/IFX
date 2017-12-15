import pandas as pd
from tqdm import tqdm

from django.core.management.base import BaseCommand

from movies.models import Field


class Command(BaseCommand):
    help = "Import fields."

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
            o = Field()
            o.fid = row.lif
            o.title = row.descr
            if not options['readonly']:
                o.save()
            progress.update(1)

        progress.close()
