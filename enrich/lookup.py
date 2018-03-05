from collections import Counter

from editing_logs.api import Recorder
from enrich.models import Suggestion, Source
from enrich.wikidata import get_wikidata_result, TooManyResults, NoResults, \
    get_props_by_pids
from ifx.base_models import WikiDataEntity
from links.models import LinkType, Link


class Undo(Exception):
    pass


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
    # TODO: update links
    qs = LinkType.objects.exclude(wikidata_id=None)
    link_types = {lt.wikidata_id: lt for lt in qs}
    props = get_props_by_pids(obj.wikidata_id, list(link_types.keys()))

    created = 0
    updated = 0
    note = f"Auto updating links for {obj.__class__.__name__} #{obj.id}"
    try:
        with Recorder(note=note) as r:
            for pid, value in props.items():
                try:
                    link = obj.links.get(type=link_types[pid])
                    if link.value != value:
                        r.record_update_before(link)
                        link.value = value
                        link.save()
                        r.record_update_after(link)
                        updated += 1
                except Link.DoesNotExist:
                    link = obj.links.create(
                        type=link_types[pid],
                        value=value,
                    )
                    r.record_addition(link)
                    created += 1
            if not created and not updated:
                raise Undo()
    except Undo:
        pass
    return Counter(updated=updated, created=created)
