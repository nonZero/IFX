from django.db import models
from django.utils.translation import ugettext_lazy as _


class UndeletableQueryset(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def deleted(self):
        return self.filter(active=False)


class Undeletable(models.Model):
    active = models.BooleanField(default=True)

    objects = UndeletableQueryset.as_manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.active = False
        return self.save()


class WikiDataEntity(models.Model):
    """A model containing a WikiData reference."""

    class Status:
        ASSIGNED = 10
        TO_BE_CREATED = 50
        NOT_APPLICABLE = 999

        choices = (
            (ASSIGNED, _('assigned')),
            (TO_BE_CREATED, _('Pending creation of a new Wikidata ID')),
            (NOT_APPLICABLE, _('N/A (should not hava a wikidata ID)')),
        )

    wikidata_status = models.PositiveIntegerField(choices=Status.choices,
                                                  null=True, blank=True)
    wikidata_id = models.CharField(max_length=50, null=True, blank=True,
                                   unique=True)

    class Meta:
        abstract = True
