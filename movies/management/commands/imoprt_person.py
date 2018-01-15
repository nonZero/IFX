import pandas as pd
from tqdm import tqdm

from django.core.management.base import BaseCommand

from movies.models import Tag, Field, Tag_Field, models


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
        progress = tqdm(total=len(df))
        for i, row in df.iterrows():
            try:
                if not str(row.book_id)[0].isdigit():
                    f = Field.objects.get(fid=row.lif)
                    t = Tag.objects.get(tid=row.book_id[1:])
                    tf = Tag_Field(tag = t, field = f, title=row.strans_id, lang=row.lang_id)
                    if not options['readonly']:
                        tf.save()
                # else:
                #     m = Movie.objects.get(bid=row.book_id)
                #     f = Field.objects.get(fid=row.lif)
                #     mf = Movie_Field(movie = m, field = f, title=row.strans_id, lang=row.lang_id)
                #     if not options['readonly']:
                #         mf.save()
            except models.ObjectDoesNotExist:
                # log error to server?
                print("\nTag or Field was not found in DB, line=" + str(i))
            finally:
                progress.update(1)
        progress.close()
