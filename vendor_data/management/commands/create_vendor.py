import requests
from django.core.management.base import BaseCommand
from django.db.models import Q

from vendor_data import models


class Command(BaseCommand):
    help = "Creates a vendor from wikidata property ID"

    def add_arguments(self, parser):
        parser.add_argument('pid')
        parser.add_argument('key')

    def handle(self, pid: str, key: str, *args, **options):
        assert pid[0] == "P", pid
        assert pid[1:].isnumeric(), pid
        assert not models.Vendor.objects.filter(
            Q(pid=pid) | Q(key=key)).exists()

        url = f"https://www.wikidata.org/wiki/Special:EntityData/{pid}.json"
        data = requests.get(url).json()
        e = data['entities'][pid]
        s = e['claims']['P1630'][0]['mainsnak']['datavalue']['value']
        v = models.Vendor(
            key=key,
            pid=pid,
            title=e['labels']['he']['value'],
            template=s,
        )
        v.full_clean()
        v.save()
        print(f"Created vendor #{v.id}: {v.key}; {v.title}")
