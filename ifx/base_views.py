from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from editing_logs.api import Recorder
from enrich.lookup import create_suggestion
from enrich.tasks import lookup_suggestion_by_id
from general.templatetags.ifx import bdtitle, bdtitle_plus


class IFXMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.predispatch()
        return super().dispatch(request, *args, **kwargs)

    def predispatch(self):
        pass

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
            return bdtitle_plus(self.get_object())
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

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser and not settings.DEBUG:
            if hasattr(settings, "GOOGLE_ANALYTICS_ID"):
                d['analytics_id'] = settings.GOOGLE_ANALYTICS_ID
        return d


class DataContributorOnlyMixin(IFXMixin):
    def predispatch(self):
        if not self.request.user.is_editor():
            raise PermissionDenied()

        super().predispatch()


class EntityActionMixin(DataContributorOnlyMixin):
    def get_title(self):
        return "{}: {}".format(self.action_name, bdtitle(self.object))

    def get_breadcrumbs(self):
        return self.breadcrumbs + (
            (bdtitle(self.object), self.object.get_absolute_url()),
        )


class EntityEditMixin(EntityActionMixin):
    action_name = _("Edit")

    def form_valid(self, form):
        o = form.instance
        original = o.__class__.objects.get(id=o.id)
        if any(getattr(o, attr) != getattr(original, attr) for attr in
               self.form_class.Meta.fields):
            with Recorder(user=self.request.user,
                          note=form.cleaned_data['editing_comment']) as r:
                r.record_update_before(original)
                o.idea_modified = True
                form.save()
                r.record_update_after(o)
            messages.success(self.request, _("Updated successfully"))
            if o.title_he:
                s, created = create_suggestion(o)
                lookup_suggestion_by_id.delay(s.id)
        return redirect(o)
