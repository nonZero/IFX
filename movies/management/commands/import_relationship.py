import pandas as pd
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from tqdm import tqdm

from movies.models import Movie, Tag, Field, MovieTag, models
from people.models import Person, Role, MovieRolePerson


class Command(BaseCommand):
    help = "Import relationship."

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

        mrp_counter = 0
        mrp_duplicates = 0
        mtf_counter = 0
        bad_relationship_count = 0
        fields_removed = 0
        roles_added = 0
        count_total = 0
        count_movie_missing = 0
        duplicate_movietag = 0

        try:
            for i, row in tqdm(df.iterrows(), total=len(df)):
                count_total += 1
                try:
                    m = Movie.objects.get(idea_bid=row.book_id)
                except Movie.DoesNotExist:
                    print("Movie was not found in DB, line=" + str(i))
                    count_movie_missing += 1
                    continue

                try:
                    # Movie-Person-Role
                    p = Person.objects.get(idea_tid=row.book2_id[1:])
                    r = Role.objects.get(idea_tid=row.lif)
                    # r, created = Role.objects.get_or_create(idea_tid=row.lif)
                    # if created:
                    #     f = Field.objects.get(idea_fid=row.lif)
                    #     r.title_he = f.title
                    #     if not options['readonly']:
                    #         r.save()
                    #         roles_added += 1
                    #     f.delete()
                    #     fields_removed += 1
                    mrp = MovieRolePerson(
                        movie=m,
                        person=p,
                        role=r,
                        idea_uid=row.unique_id
                    )
                    if not options['readonly']:
                        try:
                            mrp.save()
                            mrp_counter += 1
                        except IntegrityError:
                            mrp_duplicates += 1

                except Person.DoesNotExist:
                    try:
                        t = Tag.objects.get(idea_tid=row.book2_id[1:])
                        if not options['readonly']:
                            try:
                                MovieTag.objects.get_or_create(
                                    movie=m,
                                    tag=t,
                                    idea_uid=row.unique_id,
                                )
                                mtf_counter += 1
                            except IntegrityError:
                                duplicate_movietag += 1
                    except models.ObjectDoesNotExist:
                        bad_relationship_count += 1
        finally:
            print('Report:')
            print('Total rows={}'.format(count_total))
            print('Movie_Role_Person found={}'.format(mrp_counter))
            print('Movie_Role_Person duplicate={}'.format(mrp_duplicates))
            print('Movie_Tag found={}'.format(mtf_counter))
            print('Movie_Tag duplicate ={}'.format(duplicate_movietag))
            print('Movies missing={}'.format(count_movie_missing))
            print('bad relationship count={}'.format(bad_relationship_count))
            print('fields removed ={}'.format(fields_removed))
            print('roles added ={}'.format(roles_added))
