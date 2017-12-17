import pandas as pd
import numpy as np
from tqdm import tqdm

from django.core import serializers
from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = "Export movies."

    def add_arguments(self, parser):
        parser.add_argument('f', type=str,
                            help='file path to export to')

        parser.add_argument(
            '--readonly',
            action='store_true',
            dest='readonly',
            help='Serialize it without saving to file',
    )

    def handle(self, f, **options):
        movies = Movie.objects.all()

        print('Starting exporting {} movie row(s) to file:{}'.format(
            str(len(movies)), str(f)))

        serialized_obj = serializers.serialize('json', movies)
        if not options['readonly']:
            with open(f, 'w') as fn:
                fn.write(serialized_obj)
                print('OK')
        else:
            print('Readonly mode, nothing was saved')
