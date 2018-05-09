from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from general.entities import ENTITY_CONTENT_TYPES
from links.tasks import add_links


class Vendor(models.Model):
    key = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    pid = models.CharField(max_length=50, unique=True, null=True, blank=True)
    template = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.key


class VendorGenre(models.Model):
    # property: https://www.wikidata.org/wiki/Property:P136
    # film genre: https://www.wikidata.org/wiki/Q201658
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,
                               related_name="genre")
    value = models.CharField(max_length=250)
    qid = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = (
            ('vendor', 'value'),
        )

    def __str__(self):
        return f"{self.vendor}: {self.value}"


class VendorItem(models.Model):
    class Type:
        MOVIE = 1
        PERSON = 2
        choices = (
            (MOVIE, _("movie")),
            (PERSON, _("person")),
        )

    class Status:
        NEW = 1
        TO_BE_CREATED = 5
        ASSIGNED = 10
        NOT_APPLICABLE = 999

        choices = (
            (NEW, _('New')),
            (TO_BE_CREATED, _('Pending creation of a new Wikidata ID')),
            (ASSIGNED, _('Assigned')),
            (NOT_APPLICABLE, _('N/A')),
        )

    created_at = models.DateTimeField(_('created at'), auto_now_add=True,
                                      db_index=True)

    status = models.PositiveIntegerField(choices=Status.choices,
                                         default=Status.NEW)

    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,
                               related_name="items")
    vid = models.CharField(_('vendor_id'), max_length=400)

    type = models.IntegerField(choices=Type.choices)

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,
                                     limit_choices_to=ENTITY_CONTENT_TYPES,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    entity = GenericForeignKey()

    year = models.IntegerField(_("year"), null=True, blank=True)
    duration = models.IntegerField(_("duration"), null=True, blank=True)
    title_he = models.CharField(_('Hebrew title'), max_length=300, null=True,
                                blank=True)
    title_en = models.CharField(_('English title'), max_length=300, null=True,
                                blank=True)
    summary_he = models.TextField(_('summary in Hebrew'), null=True,
                                  blank=True)
    summary_en = models.TextField(_('summary in English'), null=True,
                                  blank=True)
    editing_comment = models.TextField(_('editing comment'), null=True,
                                       blank=True)
    imdb_id = models.CharField(('imdb ID'), max_length=50, null=True,
                               blank=True)

    extra_data = JSONField(null=True, blank=True)

    genre = models.ManyToManyField(VendorGenre, related_name="items",
                                   blank=True)

    class Meta:
        unique_together = (
            ('vendor', 'vid'),
        )
        ordering = (
            '-created_at',
        )

    def __str__(self):
        return f"{self.get_type_display()}: {self.vendor.key}.{self.vid}"

    def url(self):
        if self.vendor.template:
            return self.vendor.template.replace("$1", self.vid)
        return self.vid

    def set_wikidata_id(self, id):
        assert self.entity.wikidata_id is None, self.entity
        self.entity.wikidata_status = self.entity.Status.ASSIGNED
        self.entity.wikidata_id = id
        self.entity.save()
        add_links(self.entity)
