from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from general.templatetags.ifx import bdtitle


class IFXMixin(LoginRequiredMixin):
    def get_model_plural_name(self):
        return self.model._meta.verbose_name_plural.title()

    def get_model_name(self):
        return self.model._meta.verbose_name.title()

    def get_title(self):
        if hasattr(self, 'title'):
            return self.title
        if isinstance(self, CreateView):
            return "{} {}".format(_('Create'), self.get_model_name())
        if isinstance(self, SingleObjectMixin):
            return bdtitle(self.get_object())
        if isinstance(self, MultipleObjectMixin):
            return self.get_model_plural_name()

        raise NotImplementedError()

    def get_header(self):
        if hasattr(self, 'header'):
            return self.header
        return self.get_title()

    def get_breadcrumbs(self):
        if hasattr(self, 'breadcrumbs'):
            return self.breadcrumbs

        return None
