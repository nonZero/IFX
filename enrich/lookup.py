from enrich.models import Suggestion, Source
from enrich.wikidata import get_wikidata_result, TooManyResults, NoResults, \
    get_props_by_pids
from ifx.base_models import WikiDataEntity
from links.models import LinkType


def create_suggestion(o):
    return o.suggestions.get_or_create(
        query=o.title_he,
        source=Source.WIKIDATA,
        defaults=dict(
            status=Suggestion.Status.PENDING,
        )
    )


def query_suggestion(o: Suggestion):
    try:
        en = get_wikidata_result(o.query, o.entity.WIKIDATA_CLASSIFIER_PID)
    except TooManyResults as e:
        o.status = Suggestion.Status.MANY_RESULTS
        o.result = [en.data for en in e.results]
        o.save()
        return False
    except NoResults as e:
        o.status = Suggestion.Status.NO_RESULTS
        o.result = None
        o.save()
        return False

    o.status = Suggestion.Status.FOUND_UNVERIFIED
    o.result = en.data
    o.source_key = en.id
    o.source_url = f"http://www.wikidata.org/entity/{en.id}"
    o.save()

    return o


def create_missing_links(obj: WikiDataEntity):
    link_types = {lt.wikidata_id: lt for lt in
                  LinkType.objects.exclude(wikidata_id=None)}
    props = get_props_by_pids(obj.wikidata_id, list(link_types.keys()))

    n = 0
    for pid, value in props.items():
        link, created = obj.links.get_or_create(type=link_types[pid],
                                                value=value)
        if created:
            n += 1
    return n
