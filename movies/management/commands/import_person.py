import pandas as pd
from tqdm import tqdm

from django.core.management.base import BaseCommand

from ifx.util import is_hebrew
from movies.models import Tag, Field, models
from people.models import Person


class Command(BaseCommand):
    help = "Import person."

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
        # Person.objects.all().delete()
        for i, row in tqdm(df.iterrows(), total=len(df)):
            try:
                idea_tid = row.book_id
                f = row.lif
                lang = row.lang_id
                if not str(idea_tid)[0].isdigit():
                    p, created = Person.objects.get_or_create(
                        idea_tid=idea_tid[1:]
                    )
                    title = row.strans_id
                    if f == '#127':
                        if lang == "HEB":
                            p.last_name_he = title
                        elif lang == "ENG":
                            p.last_name_en = title
                    elif f == '#128':
                        if lang == "HEB":
                            p.first_name_he = title
                        elif lang == "ENG":
                            p.first_name_en = title

                    if not options['readonly']:
                        p.save()

            except models.ObjectDoesNotExist:
                # log error to server?
                print("\nPerson was not found in DB, line=" + str(i))
