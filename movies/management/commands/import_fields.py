import pandas as pd

from django.core.management.base import BaseCommand

from movies.models import Field


class Command(BaseCommand):
    help = "Import fields."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str)

    def handle(self, f, **options):
        df = pd.read_csv(f, delimiter='\t')
        c = len(df)
        for i, row in df.iterrows():
            if i % 200 == 0:
                print(i, c, row.lif, row.descr)
            o = Field()
            o.fid = row.lif
            o.title = row.descr
            o.save()
