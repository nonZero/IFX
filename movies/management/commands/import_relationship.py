import pandas as pd
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

        progress = tqdm(total=len(df))

        for i, row in df.iterrows():
            try:
                m = Movie.objects.get(bid=row.book_id)
                if(Person.objects.exists()):
                    # Movie-Person-Role
                    p = Person.objects.get(tid=row.book2_id[1:])
                    r, created = Role.objects.get_or_create(tid=row.lif)
                    if created:
                        f = Field.objects.get(fid=row.lif)
                        r.title_he = f.title
                        if not options['readonly']:
                            r.save()
                        f = Field.objects.get(fid=row.lif).delete()
                    mpr = Movie_Role_Person(movie=m, person=p, role=r)
                    if not options['readonly']:
                        mpr.save()
                else:
                    t = Tag.objects.get(tid=row.book2_id[1:])
                    mtf = Movie_Tag_Field(movie=m, tag = t, field = f)
                    if not options['readonly']:
                        mtf.save()
            except models.ObjectDoesNotExist:
                # log error to server?
                print("Movie, Tag or Field was not found in DB, line=" + str(i))
            finally:
                progress.update(1)

        progress.close()
