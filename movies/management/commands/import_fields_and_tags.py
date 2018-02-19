import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from movies.models import Field


class Command(BaseCommand):
    help = "Import fields and tags."

    def handle(self, **options):

        with open(
                Path(settings.BASE_DIR, "movies", "data", "fields.json")) as f:
            data = json.load(f)

        with transaction.atomic():
            for fld in data:
                o = Field.objects.create(
                    fid=fld["fid"],
                    title_en=fld["title_en"],
                    title_he=fld["title_he"],
                    appears_in_short_version=fld["appears_in_short_version"],
                    short_version_order=fld["short_version_order"],
                )
                for tag in fld['tags']:
                    o.tags.create(
                        tid=tag['tid'],
                        title_en=tag['title_en'],
                        title_he=tag['title_he'],
                        type_id=tag['type_id'],
                    )
