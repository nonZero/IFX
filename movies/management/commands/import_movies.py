import pandas as pd
import random
import silly

from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = "Import movies."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str)

    def handle(self, f, **options):
        movies = pd.read_csv(f, delimiter='\t')

        for i, row in movies.iterrows():
            print(row.bid, row.title)
            o = Movie()
            o.title = row.title
            o.length = "{}.{}".format(random.randint(1, 100),
                                      random.randint(0, 99))
            o.date = silly.datetime().date()
            o.description = "\n".join(
                [silly.paragraph(), silly.paragraph(), silly.paragraph()])
            o.bid = row.bid
            o.save()
