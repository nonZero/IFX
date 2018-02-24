from django.test import TestCase

from enrich.lookup import create_suggestion, query_suggestion
from enrich.models import Suggestion
from enrich.wikidata import get_wikidata_result, TooManyResults, NoResults, \
    FILM
from movies.models import Movie


class WikidataTestCase(TestCase):
    def test_get_one_wikidata_result(self):
        q = "קלרה הקדושה"
        en = get_wikidata_result(q, FILM)
        self.assertEqual(en.id, "Q1145082")

    def test_get_many_wikidata_result(self):
        q = "אבא גנוב"
        msg = 'Too many results: Q6956016, Q12403282, Q7052172'
        with self.assertRaisesMessage(TooManyResults, msg):
            get_wikidata_result(q, FILM)

    def test_get_no_wikidata_result(self):
        q = "שדגךלחכישגךלחכישגדךלחכישגךלחכי"
        with self.assertRaises(NoResults):
            get_wikidata_result(q, FILM)


class LookupTestCase(TestCase):
    def test_query_suggestion(self):
        m = Movie.objects.create(
            idea_bid="12345",
            title_he="קלרה הקדושה",
        )
        o, created = create_suggestion(m)
        query_suggestion(o)

        self.assertEqual(o.status, Suggestion.Status.FOUND_UNVERIFIED)
        self.assertEqual(o.source_key, "Q1145082")
