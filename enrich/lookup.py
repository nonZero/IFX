from enrich.models import Suggestion, Source
from enrich.wikidata import get_wikidata_result, TooManyResults, NoResults


def create_suggestion(m):
    return Suggestion.objects.create(
        status=Suggestion.Status.PENDING,
        entity=m,
        query=m.title_he,
        source=Source.WIKIDATA,
    )


def query_suggestion(o: Suggestion):
    try:
        en = get_wikidata_result(o.query)
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
