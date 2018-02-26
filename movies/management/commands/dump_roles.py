import json

from django.core.management.base import BaseCommand

from people.models import Role


def get_roles():
    for r in Role.objects.all():
        yield {
            'idea_tid': r.idea_tid,
            'title_en': r.title_en,
            'title_he': r.title_he,
            'appears_in_short_version': r.appears_in_short_version,
            'short_version_order': r.short_version_order,
            'wikidata_id': r.wikidata_id,
            'wikidata_status': r.wikidata_status,
        }


class Command(BaseCommand):
    help = "Dump roles as json"

    def handle(self, **options):
        data = list(get_roles())
        print(json.dumps(data, indent=2))
