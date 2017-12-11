import pandas as pd

from django.core.management.base import BaseCommand

from movies.models import Tag


class Command(BaseCommand):
    help = "Import tags."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str)

    def handle(self, f, **options):
        tags = pd.read_csv(f, delimiter='\t')

        for i, row in tags.iterrows():
            print(row.book_id_s, row.title)
            o = Tag()
            o.title = row.title
            o.bid = row.book_id_s
            o.save()
