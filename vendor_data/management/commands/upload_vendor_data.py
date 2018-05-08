import time
from collections import Counter

import json
import logging
import requests
from django.core.management.base import BaseCommand

from users.models import User
from vendor_data import models
from wikidata_edit.upload import upload_movie

logger = logging.getLogger(__name__)

SPARQL = """SELECT ?item WHERE {{?item wdt:{pid} '{value}'.}}"""


def simple_query(query):
    r = requests.get("https://query.wikidata.org/sparql", {
        'query': query,
        'format': 'json',
    })
    r.raise_for_status()
    return r.json()['results']['bindings']


def lookup_wikidata_id_by_prop(pid, value):
    q = SPARQL.format(pid=pid, value=value.replace("'", "\\'"))
    resp = simple_query(q)
    return resp[0]['item']['value'] if resp else None


def lookup_wikidata_id_by_imdb_id(imdb_id):
    return lookup_wikidata_id_by_prop("P345", imdb_id)


class Command(BaseCommand):
    help = "Matches vendor and IFX data"

    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, email, *args, **options):
        u = User.objects.get(email=email)
        oauth1 = u.get_wikidata_oauth1()

        c = Counter()
        qs = models.VendorItem.objects.filter(
            type=models.VendorItem.Type.MOVIE,
            object_id__isnull=False,
            imdb_id__isnull=False,
        )
        total = qs.count()
        print(f"checking {total} items")

        try:
            for i, o in enumerate(qs):  # type: (int, models.VendorItem)
                if o.entity.wikidata_id is not None:
                    c['exists'] += 1
                    continue

                logger.info(
                    f"Processing {i + 1}/{total}, #{o.id}={o.entity.id}: {o.title_he}")

                wikidata_id = lookup_wikidata_id_by_prop(o.vendor.pid, o.vid)
                if wikidata_id:
                    logger.info(f"FOUND BY VENDOR ID: {wikidata_id}")
                    o.set_wikidata_id(wikidata_id)
                    c['found_by_vid'] += 1
                    continue

                if o.imdb_id:
                    wikidata_id = lookup_wikidata_id_by_imdb_id(o.imdb_id)
                    if wikidata_id:
                        logger.info(f"FOUND BY IMDB_ID! {wikidata_id}")
                        o.set_wikidata_id(wikidata_id)
                        continue

                logger.info("Uploading...")

                labels = {}
                if o.title_he:
                    labels['he'] = o.title_he
                if o.title_en:
                    labels['en'] = o.title_en
                elif o.entity.title_en:
                    labels['en'] = o.entity.title_en
                descs = {}
                descs[
                    'en'] = f"{o.year} Israeli film" if o.year else "Israeli film"
                descs[
                    'he'] = f"סרט ישראלי משנת {o.year}" if o.year else "סרט ישראלי"

                ids = {o.vendor.pid: o.vid}
                if o.imdb_id:
                    ids['P345'] = o.imdb_id

                aliases = None
                if o.title_he != o.entity.title_he:
                    aliases = [['he', o.entity.title_he]]
                    logger.info(f"NEED ALIAS: {wikidata_id}")
                    c['need alias'] += 1

                resp = upload_movie(oauth1, labels, descs, ids, o.year,
                                    o.duration, aliases)
                if resp.get('success') != 1:
                    msg = "Error uploading data to wikidata\n"
                    logger.error(msg + json.dumps(resp, indent=2))
                    c['error'] += 1
                    time.sleep(1)
                else:
                    id = resp['entity']['id']
                    print(f"New Wikidata ID {id} for movie #{o.entity.id}.")
                    o.set_wikidata_id(id)
                    c['added'] += 1
                    time.sleep(0.1)

        finally:
            for k, v in sorted(c.items()):
                print(k, v)
