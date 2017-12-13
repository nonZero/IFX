import pandas as pd

from django.core.management.base import BaseCommand

from movies.models import Movie, Tag, Field, Movie_Tag_Field


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
            t = Tag.objects.get(tid=row.book2_id[1:])
            f = Field.objects.get(fid=row.lif)
            mtf = Movie_Tag_Field(movie=m, tag = t, field = f)
            if i % 200 == 0:
                print(m, t, f)
            mtf.save()
