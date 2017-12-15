import pandas as pd
from tqdm import tqdm

from django.core.management.base import BaseCommand

from movies.models import Movie, Tag, Field, Movie_Tag_Field


class Command(BaseCommand):
    help = "Import relationship."

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
            m = Movie.objects.get(bid=row.book_id)
            t = Tag.objects.get(tid=row.book2_id[1:])
            f = Field.objects.get(fid=row.lif)
            mtf = Movie_Tag_Field(movie=m, tag = t, field = f)
            if not options['readonly']:
                mtf.save()
            progress.update(1)

        progress.close()
