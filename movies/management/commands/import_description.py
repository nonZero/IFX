import pandas as pd
from django.core.exceptions import ObjectDoesNotExist

from django.core.management.base import BaseCommand
from tqdm import tqdm

from movies.models import Movie, Description


class Command(BaseCommand):
    help = "Import description."

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
        df_sorted = df.sort_values(["book_id", "counter"])
        progress = tqdm(total=len(df))

        count_total = 0
        count_movie_missing = 0
        count_movie_found = 0
        count_new_decription = 0
        count_nan = 0
        count_not_digit = 0
        count_concatenation = 0

        for i, row in df_sorted.iterrows():
            count_total += 1
            if str(row.book_id).isdigit():
                try:
                    movie = Movie.objects.get(bid=row.book_id)
                    if movie:
                        count_movie_found += 1
                        o, created = Description.objects.get_or_create(movie=movie, lang=row.lang_id)
                        if created:
                            count_new_decription += 1
                            o.movie = movie
                            o.lang = row.lang_id

                        o.summery += str(row.summary)
                        if pd.isnull(row.counter):
                            count_nan += 1
                        elif not str(row.counter).isdigit():
                            count_not_digit += 1
                        elif int(row.counter) > 1:
                            count_concatenation += 1

                        if not options['readonly']:
                            o.save()

                except ObjectDoesNotExist:
                    count_movie_missing += 1

            progress.update(1)
        progress.close()

        print('Report:')
        print('Total rows={}'.format(count_total))
        print('Movies found={}'.format(count_movie_found))
        print('Movies missing={}'.format(count_movie_missing))
        print('New description rows={}'.format(count_new_decription))
        print('Rows with counter NaN={}'.format(count_nan))
        print('Rows with counter not integer={}'.format(count_not_digit))
        print('Rows with counter for concatenation={}'.format(count_concatenation))
