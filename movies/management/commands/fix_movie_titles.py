from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import F
from tqdm import tqdm

from editing_logs.api import Recorder
from ifx.util import is_hebrew, is_english
from movies.models import Movie


def clear(m: Movie, attr):
    with Recorder(note="Auto remove title") as r:
        r.record_update_before(m)
        setattr(m, attr, None)
        m.idea_modified = True
        m.save()
        r.record_update_after(m)


class Command(BaseCommand):
    help = "Fix movie english/hebrew titles."

    def handle(self, **options):
        c = Counter()
        try:
            qs = Movie.objects.filter(title_he=F('title_en'),
                                      title_he__isnull=False)
            for m in tqdm(qs):
                c['found'] += 1
                if is_hebrew(m.title_he):
                    clear(m, 'title_en')
                    c['hebrew'] += 1
                elif is_english(m.title_en):
                    clear(m, 'title_he')
                    c['english'] += 1
                else:
                    c['unknown'] += 1

        finally:
            for k, v in c.items():
                print(k, v)
