from urllib.parse import quote

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField

from general.entities import ENTITY_CONTENT_TYPES
from people.models import Person


class Source:
    WIKIDATA = 1
    WIKIPEDIA = 2
    VIAF = 3

    CHOICES = (
        (WIKIDATA, _('WikiData')),
        (WIKIPEDIA, _('Wikipedia')),
        (VIAF, _('VAIF')),
    )


# class Identity(models.Model):
#     source_type = models.CharField(max_length=300, choices=SOURCE_TYPE_CHOICES,
#                                    default='VIAF')
#     source_value = models.CharField(max_length=300, null=True, blank=True)
#
#     STATUS_CHOICES = (
#         ('NEW', 'NEW'),
#         ('ACCEPTED', 'ACCEPTED'),
#         ('REJECTED', 'REJECTED'),
#         ('UNDER_DISCUSSION', 'UNDER_DISCUSSION'),
#     )
#     status = models.CharField(max_length=300, choices=STATUS_CHOICES,
#                               default='NEW')
#
#     notes = models.TextField(null=True, blank=True)
#     score = models.IntegerField(null=True, blank=True)
#
#     content_type = models.ForeignKey(
#         ContentType,
#         on_delete=models.CASCADE,
#         verbose_name=_('content person'),
#         limit_choices_to=ENTITY_CONTENT_TYPES,
#         null=True,
#         blank=True,
#     )
#     object_id = models.PositiveIntegerField(
#         verbose_name=_('related object'),
#         null=True,
#     )
#     entity = GenericForeignKey('content_type', 'object_id')
#     # content_object = GenericForeignKey()
#
#     # https://en.wikipedia.org/w/index.php?search=Edward+Dmytryk
#     # http://viaf.org/viaf/search?query=local.personalNames+all+%22Edward%20Dmytryk%22&sortKeys=holdingscount&recordSchema=BriefVIAF
#
#     URIs = {
#         WIKIDATA: 'https://en.wikipedia.org/w/index.php?search={}',
#         WIKIPEDIA: 'https://www.wikimedia.org/',
#         VIAF: 'http://viaf.org/viaf/search?query=local.personalNames+all+"{}"&sortKeys=holdingscount&recordSchema=BriefVIAF',
#     }
#
#     def enrich_object(self):
#         print(self.source_type)
#         uri = self.URIs[self.source_type]
#         print(uri)
#
#     def get_wikipedia_info(self):
#         try:
#             # TODO: movie support
#             p = Person.objects.get(pk=self.object_id)
#             name = p.name_en
#             try:
#                 url = WIKIPEDIA.page(name).url
#                 print(url)
#             except WIKIPEDIA.exceptions.DisambiguationError as e:
#                 print(e.options)
#         except:
#             print('Not found, Id={}'.format(self.object_id))
#     pass


class Suggestion(models.Model):
    class Status:
        ''''''

        '''A new suggestion task pending web query'''
        PENDING = 1

        '''Critical error state, message saved in `error_message` property'''
        ERROR = 5

        NO_RESULTS = 10
        MANY_RESULTS = 11

        FOUND_UNVERIFIED = 100
        VERIFIED = 200

        REJECTED = 500

        CHOICES = (
            (PENDING, _('pending')),
            (ERROR, _('error')),
            (NO_RESULTS, _('no results')),
            (MANY_RESULTS, _('too many results')),
            (FOUND_UNVERIFIED, _('found (unverified)')),
            (VERIFIED, _('verified')),
            (REJECTED, _('rejected')),
        )

        TAG = dict((
            (PENDING, 'default'),
            (ERROR, 'danger'),
            (NO_RESULTS, 'danger'),
            (MANY_RESULTS, 'danger'),
            (FOUND_UNVERIFIED, 'success'),
            (VERIFIED, 'success'),
            (REJECTED, 'warning'),
        ))

        INCOMPLETE = (
            PENDING,
            ERROR,
            NO_RESULTS,
            MANY_RESULTS,
            FOUND_UNVERIFIED,
        )

    status = models.IntegerField(_('status'), choices=Status.CHOICES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=ENTITY_CONTENT_TYPES,
                                     verbose_name=_('entity type')
                                     )
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey()

    query = models.CharField(_('query string'), max_length=300)

    source = models.IntegerField(_('source'), choices=Source.CHOICES)
    source_key = models.CharField(max_length=500, null=True)
    source_url = models.URLField(null=True)

    '''Save web query result'''
    result = JSONField(null=True)

    error_message = models.TextField(null=True)

    class Meta:
        verbose_name = _("suggestion")
        verbose_name_plural = _("suggestions")

    def found(self):
        return self.status in (
        self.Status.VERIFIED, self.Status.FOUND_UNVERIFIED)

    def status_tag(self):
        return self.Status.TAG[self.status]

    # def __str__(self):
    #     return f"{self.id}|{self.entity}|{self.get_source_display}|{self.get_status_display}"

    def search_url(self):
        # TODO: per data source
        return "https://www.wikidata.org/w/index.php?search={}".format(
            quote(self.query)
        )
