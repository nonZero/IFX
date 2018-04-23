from collections import Counter, namedtuple
from typing import Iterator

from SPARQLWrapper import SPARQLWrapper, JSON

from editing_logs.api import Recorder
from enrich.models import Suggestion, Source
from enrich.wikidata import get_wikidata_result, TooManyResults, NoResults, \
    get_props_by_pids, get_sitelinks_by_linktype
from ifx.base_models import WikiDataEntity
from links.models import LinkType, Link

MOVIE_SPARQL = """
SELECT ?rel ?movie ?movieLabelHe ?movieLabelEn WHERE {
  ?movie wdt:P31 wd:Q11424.
  ?movie ?rel wd:%s.
  OPTIONAL {?movie rdfs:label ?movieLabelHe filter (lang(?movieLabelHe) = "he")}.
  OPTIONAL {?movie rdfs:label ?movieLabelEn filter (lang(?movieLabelEn) = "en")}.
}
"""


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


SparqlMovie = namedtuple('SparqlMovie', 'rel,id,he,en')


def get_movies_for_person(wikidata_id: str) -> Iterator[SparqlMovie]:
    assert wikidata_id[0] in "QS"
    assert wikidata_id[1:].isdigit()
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = MOVIE_SPARQL % wikidata_id
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        yield SparqlMovie(
            rel=result["rel"]["value"].split("/")[-1],
            id=result["movie"]["value"].split("/")[-1],
            he=result.get("movieLabelHe", {}).get("value"),
            en=result.get("movieLabelEn", {}).get("value"),
        )


def create_sitelinks(obj: WikiDataEntity):
    lt = {item.slug.split('_')[1]: item for item in LinkType.objects.filter(slug__startswith='sitelinks_')}

    props = get_sitelinks_by_linktype(obj.wikidata_id, list(lt.keys()))

    created = 0
    updated = 0
    note = f"Auto updating links for {obj.__class__.__name__} #{obj.id}"
    try:
        with Recorder(note=note) as r:
            for key, value in props.items():
                try:
                    link = obj.links.get(type=lt[key])
                    if link.value != value:
                        r.record_update_before(link)
                        link.value = value
                        link.save()
                        r.record_update_after(link)
                        updated += 1
                except Link.DoesNotExist:
                    link = obj.links.create(
                        type=lt[key],
                        value=value,
                    )
                    r.record_addition(link)
                    created += 1
            if not created and not updated:
                raise Undo()
    except Undo:
        pass
    return Counter(updated=updated, created=created)
