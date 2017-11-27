import random

import silly
from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = "Create new movies."

    def add_arguments(self, parser):
        parser.add_argument('n', type=int)

    def handle(self, n, **options):
        for i in range(n):
            o = Movie()
            o.title = silly.a_thing()
            o.length = "{}.{}".format(random.randint(1, 100),
                                      random.randint(0, 99))
            o.date = silly.datetime().date()
            o.description = "\n".join(
                [silly.paragraph(), silly.paragraph(), silly.paragraph()])
            o.save()
