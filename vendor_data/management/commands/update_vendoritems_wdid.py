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
                qs = v.items.filter(wikidata_id=None)
                vids = qs.values_list('vid', flat=True).order_by('vid')
                d = dict(vids_query(v.pid, vids))
                print(v, len(d), '/', len(vids))
                for vid, wdid in d.items():
                    o = v.items.get(vid=vid)  # type: models.VendorItem
                    o.wikidata_id = wdid
                    o.save()
                    if o.entity:
                        if o.entity.wikidata_id is None:
                            o.entity.wikidata_id = wdid
                            o.entity.wikidata_status = o.entity.Status.ASSIGNED
                            o.entity.save()
                            c['movies!'] += 1
                        else:
                            if o.entity.wikidata_id != wdid:
                                logger.error(f"Wikidata ID mismatch! vid={vid}:{wdid} movie={o.entity}:{o.entity.wikidata_id}")
                                c['mismatch!!'] += 1
                    c[v.key] += 1
                    c['total'] += 1
        finally:
            print("-" * 20)
            for k, v in c.most_common():
                print(k, v)
