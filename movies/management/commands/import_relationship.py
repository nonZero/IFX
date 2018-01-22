import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from tqdm import tqdm

from django.core.management.base import BaseCommand

from movies.models import Movie, Tag, Field, Movie_Tag_Field, models, Person, Role, Movie_Role_Person


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
        mtf_counter = 0
        bad_relationship_count = 0
        fields_removed = 0
        roles_added = 0
        count_total = 0
        count_movie_missing = 0
        
        progress = tqdm(total=len(df))

        for i, row in df.iterrows():
            count_total += 1
            try:
                m = Movie.objects.get(bid=row.book_id)
                try:
                    # Movie-Person-Role
                    p = Person.objects.get(tid=row.book2_id[1:])
                    r, created = Role.objects.get_or_create(tid=row.lif)
                    if created:
                        f = Field.objects.get(fid=row.lif)
                        r.title_he = f.title
                        if not options['readonly']:
                            r.save()
                            roles_added+=1
                        f.delete()
                        fields_removed+=1
                    mrp = Movie_Role_Person(movie=m, person=p, role=r)
                    if not options['readonly']:
                        mrp.save()
                        mrp_counter+=1
                except:
                    try:
                        f = Field.objects.get(fid=row.lif)
                        t = Tag.objects.get(tid=row.book2_id[1:])
                        mtf = Movie_Tag_Field(movie=m, tag = t, field = f)
                        if not options['readonly']:
                            mtf.save()
                            mtf_counter+=1
                    except models.ObjectDoesNotExist:
                        bad_relationship_count+=1
            except models.ObjectDoesNotExist:
                # log error to server?
                print("Movie was not found in DB, line=" + str(i))
                count_movie_missing+=1
            finally:
                progress.update(1)
        progress.close()

        print('Report:')
        print('Total rows={}'.format(count_total))
        print('Movie_Role_Person found={}'.format(mrp_counter))
        print('Movie_Tag_Field found={}'.format(mtf_counter))
        print('Movies missing={}'.format(count_movie_missing))
        print('bad relationship count={}'.format(bad_relationship_count))
        print('fields removed ={}'.format(fields_removed))
        print('roles added ={}'.format(roles_added))