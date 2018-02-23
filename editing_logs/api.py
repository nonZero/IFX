import datetime

from django.db.models import Model
from django.db.transaction import Atomic

from editing_logs.models import LogItem, LogItemRow

def fix(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    return x


def get_data(entity):
    return [(fld, fix(getattr(entity, fld))) for fld in entity.FIELDS_TO_LOG]


class Recorder(Atomic):

    def __init__(self, user=None, note=None, using=None, savepoint=None):
        self.user = user
        self.note = note
        super().__init__(using, savepoint)

    def __enter__(self):
        super().__enter__()
        self.log_item = LogItem.objects.create(user=self.user, note=self.note)
        return self

    def add_row(self, op, entity, data):
        self.log_item.rows.create(
            op=op,
            entity=entity,
            data=data,
        )

    def record_addition(self, entity):
        data = get_data(entity)
        self.add_row(
            op=LogItemRow.Op.ADD,
            entity=entity,
            data=data,
        )

    def record_update_before(self, entity):
        assert not hasattr(self, '_current_entity')
        self._current_entity = entity
        self._current_entity_data = get_data(entity)

    def record_update_after(self, entity):
        assert hasattr(self, '_current_entity')
        assert entity == self._current_entity, (
            "Mismatch:", entity, self._current_entity)
        old = self._current_entity_data
        updated = get_data(entity)

        data = [(a[0], a[1], b[1]) for a, b in zip(old, updated) if
                a[1] != b[1]]

        self.add_row(
            op=LogItemRow.Op.UPDATE,
            entity=entity,
            data=data,
        )

        del self._current_entity
        del self._current_entity_data

    def record_delete(self, entity):
        data = get_data(entity)
        self.add_row(
            op=LogItemRow.Op.DELETE,
            entity=entity,
            data=data,
        )

    def create(self, kls: Model, **kwargs):
        o = kls.objects.create(**kwargs)
        self.record_addition(o)
        return o

    def save(self, o, **kwargs):
        self.record_update_before(o)
        for k, v in kwargs.items():
            setattr(o, k, v)
        self.record_update_after(o)
        return o

    def soft_delete(self, o):
        self.record_delete(o)
        return o.soft_delete()
