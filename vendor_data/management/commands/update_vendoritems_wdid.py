import itertools
from collections import Counter

import logging
from django.core.management.base import BaseCommand

from simple_sparql.query import simple_query
from vendor_data import models

logger = logging.getLogger(__name__)

SPARQL = "SELECT ?id ?item WHERE {{?item wdt:{pid} ?id.}} VALUES (?id) {{\n{values}\n}}"


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def vids_query(pid, vids, page_by=250):
    for group in grouper(vids, page_by):
        q = SPARQL.format(
            pid=pid,
            values="\n".join(f'  ("{vid}")' for vid in group)
        )
        resp = simple_query(q)
        yield from ((x['id']['value'], x['item']['value'].split("/")[-1]) for x
                    in resp)


class Command(BaseCommand):
    help = "Matches vendor and IFX data"

    def handle(self, *args, **options):
        c = Counter()
        try:
            for v in models.Vendor.objects.all():
                qs = v.items.exclude(wikidata_id=None)
                vids = qs.values_list('vid', flat=True).order_by('vid')
                d = dict(vids_query(v.pid, vids))
                print(v, len(d), '/', len(vids))
                for vid, wdid in d.items():
                    o = v.items.get(vid=vid)  # type: models.VendorItem
                    o.wikidata_id = wdid
                    o.save()
                    # if o.entity:
                    #     self.entity.wikidata_id is None or self.entity.wikidata_id == id
                    #     self.entity.wikidata_status = self.entity.Status.ASSIGNED
                    #     self.entity.wikidata_id = id
                    #     self.entity.save()
                    # else:
                    c[v.key] += 1
                    c['total'] += 1
        finally:
            for k, v in c.most_common():
                print(k, v)
