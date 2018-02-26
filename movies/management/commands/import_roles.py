import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from people.models import Role


class Command(BaseCommand):
    help = "Import roles."

    def handle(self, **options):
        source = Path(settings.BASE_DIR, "people", "data", "roles.json")
        with source.open() as f:
            data = json.load(f)

        with transaction.atomic():
            for r in data:
                o, created = Role.objects.update_or_create(
                    idea_tid=r["idea_tid"],
                    defaults=dict(
                        title_en=r["title_en"],
                        title_he=r["title_he"],
                        appears_in_short_version=r["appears_in_short_version"],
                        short_version_order=r["short_version_order"],
                        wikidata_status=r["wikidata_status"],
                        wikidata_id=r["wikidata_id"],
                    )
                )
