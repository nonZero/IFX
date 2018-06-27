import logging
from django.db import migrations
from django.db.models.expressions import RawSQL

logger = logging.getLogger(__name__)


def forwards(apps, schema_editor):
    Movie = apps.get_model("movies", "Movie")
    VendorItem = apps.get_model("vendor_data", "VendorItem")

    qs0 = Movie.objects.exclude(wikidata_id=None)
    qs = VendorItem.objects.filter(object_id__in=qs0, wikidata_id=None)
    SQL = "select wikidata_id from movies_movie m where m.id = vendor_data_vendoritem.object_id"
    f = RawSQL(SQL, ())
    result = qs.update(wikidata_id=f)
    logger.info(f"Updated wikidata ids: {result}")


class Migration(migrations.Migration):
    dependencies = [
        ('vendor_data', '0003_auto_20180524_1326'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]
