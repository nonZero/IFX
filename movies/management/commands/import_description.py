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

        for i, row in df_sorted.iterrows():
            count_total += 1
            if str(row.book_id).isdigit():
                try:
                    movie = Movie.objects.get(bid=row.book_id)
                    if movie:
                        count_movie_found += 1

                        if pd.isnull(row.counter) or \
                                not str(row.counter).isdigit():
                            print('Error - counter field is NaN or not digit')
                            continue

                        if pd.isnull(row.lang_id):
                            print('Error - language field is NaN')
                            continue

                        if (row.lang_id.isdigit() and int(row.lang_id) == 1) or \
                            row.lang_id == 'HEB':  # he
                            # movie.summary_he += str(row.summary)
                            self.update_summary_he(movie, row.summary, row.counter)
                        elif (row.lang_id.isdigit() and int(row.lang_id) == 2) or \
                            row.lang_id == 'ENG':  # en
                            # movie.summary_en += str(row.summary)
                            self.update_summary_en(movie, row.summary, row.counter)

                        if not options['readonly']:
                            movie.save()

                except ObjectDoesNotExist:
                    count_movie_missing += 1

            progress.update(1)
        progress.close()

        print('Report:')
        print('Total rows={}'.format(count_total))
        print('Movies found={}'.format(count_movie_found))
        print('Movies missing={}'.format(count_movie_missing))

    @staticmethod
    def update_summary_he(movie, summary, counter):
        if int(counter) == 1:
            movie.summary_he = summary
        else:
            movie.summary_he += summary

    @staticmethod
    def update_summary_en(movie, summary, counter):
        if int(counter) == 1:
            movie.summary_en = summary
        else:
            movie.summary_en += summary
