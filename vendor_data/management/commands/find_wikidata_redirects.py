import itertools
from collections import Counter

import logging
from django.core.management.base import BaseCommand

from movies.models import Movie
from simple_sparql.query import simple_query

logger = logging.getLogger(__name__)

SPARQL = "SELECT ?a ?b {{ VALUES ?a {{\n{values}\n}} ?a owl:sameAs ?b .}}"


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def tail(x):
    return x['value'].split("/")[-1]


def find_redirects_query(qids, page_by=250):
    for group in grouper(qids, page_by):
        q = SPARQL.format(
            values="\n".join(f'  wd:{vid}' for vid in group)
        )
        resp = simple_query(q)
        yield from ((tail(x['a']), tail(x['b'])) for x in resp)


class Command(BaseCommand):
    help = "Finds and fixes entity redirects"

    def handle(self, *args, **options):
        c = Counter()
        try:
            qs = Movie.objects.exclude(wikidata_id=None)
            print(f"Checking {qs.count()} entities.")
            qids = qs.values_list('wikidata_id', flat=True)
            for old, new in find_redirects_query(qids):
                print(old, "==>", new)
                o = Movie.objects.get(wikidata_id=old)
                o.wikidata_id = new
                o.save()
                c['fixed'] += 1
        finally:
            for k, v in c.most_common():
                print(k, v)
