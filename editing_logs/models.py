from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.forms import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class LogItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"[{self.id}] {self.user}@{self.created_at}"


class LogItemRow(models.Model):
    class Op:
        ADD = 1
        UPDATE = 2
        DELETE = 3

        choices = (
            (ADD, _("add")),
            (UPDATE, _("update")),
            (DELETE, _("delete")),
        )

    log_item = models.ForeignKey(LogItem, related_name='rows',
                                 on_delete=models.CASCADE)

    op = models.IntegerField(choices=Op.choices)

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey()

    data = JSONField()
