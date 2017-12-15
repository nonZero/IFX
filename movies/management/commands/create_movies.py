import random
from tqdm import tqdm
import silly
from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = "Create new movies."

    def add_arguments(self, parser):
        parser.add_argument('n', type=int)

        parser.add_argument(
            '--readonly',
            action='store_true',
            dest='readonly',
            help='Parse it without saving to database',
        )

    def handle(self, n, **options):
        last_bid = Movie.objects.latest('bid').bid

        progress = tqdm(total=n)

        for i in range(n):
            o = Movie()
            o.bid = last_bid + i + 1
            o.title = silly.a_thing()
            o.year = random.randint(1900, 2100)
            o.lang = random.choice(['Heb', 'Eng', 'Unknown'])
            o.full_clean()

            if not options['readonly']:
                o.save()
            progress.update(1)

        progress.close()