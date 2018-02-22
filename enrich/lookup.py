from enrich.models import Suggestion, Source
from enrich.wikidata import get_wikidata_result, TooManyResults, NoResults


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
