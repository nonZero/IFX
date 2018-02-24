from django.forms import ModelChoiceField
from django.utils.translation import get_language


class LocaleModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "title_" + get_language())
