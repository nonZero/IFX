from celery import shared_task

from enrich.lookup import query_suggestion
from enrich.models import Suggestion


@shared_task
def lookup_suggestion_by_id(id):
    o = Suggestion.objects.get(id=id)
    query_suggestion(o)
    return o.status
