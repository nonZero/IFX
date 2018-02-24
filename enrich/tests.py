from django.test import TestCase

from enrich.lookup import create_suggestion, query_suggestion
from enrich.models import Suggestion, Source
from enrich.verify import verify_movie, verify_and_update_movie, \
    verify_suggestion
from enrich.wikidata import get_wikidata_result, TooManyResults, NoResults, \
    FILM
from movies.models import Movie
from people.models import Role, Person


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


class VerifyTestCase(TestCase):
    def setUp(self):
        self.director = Role.objects.create(
            title_en='Director',
            wikidata_id='P57',
        )
        self.m = Movie.objects.create(
            title_he="קלרה הקדושה",
        )
        self.p = Person.objects.create(name_en='Ari Folman')
        self.m.people.create(
            person=self.p,
            role=self.director
        )

    def test_verify_movie_correct(self):
        result = verify_movie(self.m, "Q1145082")

        expected = {
            self.m: "Q1145082",
            self.p: "Q653645",
        }

        self.assertEqual(result, expected)

    def test_verify_movie_wrong(self):
        m = Movie.objects.create(
            title_he="אחים",
        )
        m.people.create(
            person=Person.objects.create(name_he='יגאל נידאם'),
            role=self.director
        )

        result = verify_movie(m, "Q948635")

        self.assertEqual(result, {})

    def test_verify_and_update_movie(self):
        self.assertIsNone(self.m.wikidata_id)
        self.assertIsNone(self.p.wikidata_id)

        changed, facts = verify_and_update_movie(self.m, "Q1145082")

        self.assertEqual(changed, 2)

        self.m.refresh_from_db()
        self.p.refresh_from_db()

        self.assertEqual(self.m.wikidata_status, Movie.Status.ASSIGNED)
        self.assertEqual(self.m.wikidata_id, "Q1145082")
        self.assertEqual(self.p.wikidata_status, Movie.Status.ASSIGNED)
        self.assertEqual(self.p.wikidata_id, "Q653645")

        changed, facts = verify_and_update_movie(self.m, "Q1145082")
        self.assertEqual(changed, 0)

    def test_verify_suggestion(self):
        qid = "Q1145082"

        s = Suggestion.objects.create(
            entity=self.m,
            source=Source.WIKIDATA,
            source_key=qid,
            status=Suggestion.Status.FOUND_UNVERIFIED,
        )

        self.assertIsNone(self.m.wikidata_id)
        self.assertIsNone(self.p.wikidata_id)

        movie_verified, total_verified = verify_suggestion(s)

        assert movie_verified
        self.assertEqual(total_verified, 2)

        s.refresh_from_db()
        self.m.refresh_from_db()
        self.p.refresh_from_db()

        self.assertEqual(s.status, Suggestion.Status.VERIFIED)
        self.assertEqual(self.m.wikidata_id, qid)
        self.assertEqual(self.p.wikidata_id, "Q653645")
