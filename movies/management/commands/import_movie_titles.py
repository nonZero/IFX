from collections import Counter
from pprint import pprint

import pandas as pd
from django.core.management.base import BaseCommand
from tqdm import tqdm

from movies.models import models, Movie, Tag
from people.models import Person


class Command(BaseCommand):
    help = "Import movie titles translations."

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
        c = Counter()
        try:
            df = pd.read_csv(f, delimiter='\t')
            progress = tqdm(total=len(df))
            for i, row in df.iterrows():
                if str(row.book_id).isdigit():
                    try:
                        m = Movie.objects.get(idea_bid=row.book_id)
                        if row.lang_id == "ENG":
                            m.title_en = row.title
                        elif row.lang_id == "HEB":
                            m.title_he = row.title
                        else:
                            assert False, row
                        m.save()
                        c[row.lang_id] += 1
                    except models.ObjectDoesNotExist:
                        c['missing'] += 1
                elif row.book_id[0] == "T":
                    try:
                        p = Person.objects.get(idea_tid=row.book_id[1:])
                        if row.lang_id == "ENG":
                            # if p.name_en and p.name_en != row.title:
                            #     print(p.name_en, "!=", row.title)
                            p.name_en = row.title
                        elif row.lang_id == "HEB":
                            # if p.name_he and p.name_he != row.title:
                            #     print(p.name_he, "!=", row.title)
                            p.name_he = row.title
                        else:
                            assert False, row
                        p.save()
                        c["P" + row.lang_id] += 1
                    except models.ObjectDoesNotExist:
                        try:
                            t = Tag.objects.get(idea_tid=row.book_id[1:])
                            if row.lang_id == "ENG":
                                t.title_en = row.title
                                t.save()
                            elif row.lang_id == "HEB":
                                t.title_he = row.title
                                t.save()
                            else:
                                assert False, row
                            c["T" + row.lang_id] += 1
                        except models.ObjectDoesNotExist:
                            c['skipped'] += 1
                else:
                    c['unknown'] += 1

                progress.update(1)
            progress.close()
        finally:
            pprint(c.most_common())
