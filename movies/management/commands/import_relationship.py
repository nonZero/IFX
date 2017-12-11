import pandas as pd

from django.core.management.base import BaseCommand

from movies.models import Movie, Tag


class Command(BaseCommand):
    help = "Import relationship."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str)

    def handle(self, f, **options):
        df = pd.read_csv(f, delimiter='\t')
        c = len(df)
        for i, row in df.iterrows():
            # print (row.book_id,row.book2_id[1:] )
            m = Movie.objects.get(bid=row.book_id)
            m.tags.add(Tag.objects.get(tid=row.book2_id[1:]))
            if i % 200 == 0:
                print(i, c)
