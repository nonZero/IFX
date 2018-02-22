import json
from django.core.management.base import BaseCommand

# from movies.models import Field
#
# # Ignore some misbehaving fields
# BLACKLIST = [
#     '#729'  # דיבוב 4,
#     '#739'  # תכניה - שפה 1,
#     '#740'  # תכניה - תרגום 1,
# ]
#
#
# def get_fields():
#     for f in Field.objects.exclude(fid__in=BLACKLIST).exclude(
#             movietagfield=None):
#         yield {
#             'idea_fid': f.idea_fid,
#             'title_en': f.title,
#             'title_he': f.title,
#             'appears_in_short_version': f.appears_in_short_version,
#             'short_version_order': f.short_version_order,
#             'tags': list(get_tags(f)),
#         }
#
#
# def get_tags(f: Field):
#     for mft in f.movietagfield_set.distinct('tag'):
#         t = mft.tag
#         yield {
#             'idea_tid': t.idea_tid,
#             'title_en': t.title_en,
#             'title_he': t.title_he,
#             'type_id': t.type_id,
#         }
#

class Command(BaseCommand):
    help = "Dump fields and tags"

    def handle(self, **options):
        assert False
        data = list(get_fields())
        print(json.dumps(data, indent=2))

