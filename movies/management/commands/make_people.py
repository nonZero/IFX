import pandas as pd
from tqdm import tqdm

from django.core.management.base import BaseCommand

from movies.models import Tag, Movie_Tag_Field, Person

PERSON_FIELDS = {
    'BAMAI': 'במאי',
    '#53': 'תסריטאי',
    '#61': 'עוזר עריכה',
    '#62': 'קריין',
    '#37': 'מפיק',
    '#38': 'שחקן',
    '#41': 'צלם',
    '#42': 'עורך',
    '#44': 'מוזיקה',
    '#45': 'עורך סאונד',
    '#127': 'שם משפחה',
    '#128': 'שם פרטי',
    '#165': 'צוות',
}

class Command(BaseCommand):
    help = "Make people from Tags by Person Fields."

    def add_arguments(self, parser):
        parser.add_argument(
            '--readonly',
            action='store_true',
            dest='readonly',
            help='Parse it without saving to database',
        )

    def handle(self, **options):

        # print('Reading Movie-Field-Tag relation...')
        # count = 0
        # qs = Movie_Tag_Field.objects.all()
        # progress = tqdm(total=len(qs))
        # for item in qs:
        #     fid = item.field.fid
        #     if fid in PERSON_FIELDS:
        #         tid = item.tag.tid
        #         tag = Tag.objects.get(tid=tid)
        #         person, created = Person.objects.get_or_create(tid=tag.tid)
        #         if created:
        #             person.tid = tag.tid
        #         if tag.lang == 'he':
        #             person.name_he = tag.title
        #         else:
        #             person.name_en = tag.title
        #         count += 1
        #         if not options['readonly']:
        #             person.save()
        #     progress.update(1)
        # progress.close()
        # print('Found {} people...'.format(count))

        print('Reading Field-Tag relation...')
        count = 0
        qs = Tag_Field.objects.all()
        progress = tqdm(total=len(qs))
        for item in qs:
            fid = item.field.fid
            if fid in PERSON_FIELDS:
                tid = item.tag.tid
                tag = Tag.objects.get(tid=tid)
                person, created = Person.objects.get_or_create(tid=tag.tid)
                if created:
                    person.tid = tag.tid
                if fid == '#127':  # 'שם משפחה'
                    if tag.lang == 'he':
                        person.last_name_he = tag.title
                    else:
                        person.last_name_en = tag.title
                elif fid == '#128':  # 'שם פרטי'
                    if tag.lang == 'he':
                        person.first_name_he = tag.title
                    else:
                        person.first_name_en = tag.title

                count += 1
                if not options['readonly']:
                    person.save()

            progress.update(1)
        progress.close()
        print('Found {} people...'.format(count))

