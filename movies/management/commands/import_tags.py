import pandas as pd

from django.core.management.base import BaseCommand

from movies.models import Tag


class Command(BaseCommand):
    help = "Import tags."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str)

    def handle(self, f, **options):
        df = pd.read_csv(f, delimiter='\t')
        c = len(df)
        for i, row in df.iterrows():
            if i % 200 == 0:
                print(i, c, row.book_id_s, row.title)
            o = Tag()
            o.title = row.title
            o.tid = row.book_id_s
            o.save()
