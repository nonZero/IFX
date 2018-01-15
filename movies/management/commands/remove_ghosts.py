import pandas as pd
from tqdm import tqdm

from django.core.management.base import BaseCommand

from movies.models import Movie, Tag, Field, Movie_Tag_Field, models


class Command(BaseCommand):
    help = "Remove ghosts."

    def handle(self, **options):

        tags = Tag.objects.filter(movie_tag_field=None, tag_field=None).delete()
        print(tags)

        fields = Field.objects.filter(movie_tag_field=None, tag_field=None).delete()
        print(fields)
        # progress = tqdm(total=len(tags))
        #
        # for i, row in df.iterrows():
        #     try:
        #         m = Movie.objects.get(bid=row.book_id)
        #         t = Tag.objects.get(tid=row.book2_id[1:])
        #         f = Field.objects.get(fid=row.lif)
        #         mtf = Movie_Tag_Field(movie=m, tag = t, field = f)
        #         if not options['readonly']:
        #             mtf.save()
        #     except models.ObjectDoesNotExist:
        #         # log error to server?
        #         print("Movie, Tag or Field was not found in DB, line=" + str(i))
        #     finally:
        #         progress.update(1)
        #
        # progress.close()
