from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView

import movies.models
import people.models
from editing_logs.api import Recorder
from general.templatetags.ifx import bdtitle
from ifx.base_views import IFXMixin
from links import forms
from links.models import LinkType, Link

ENTITY_MODELS = {
    'movie': movies.models.Movie,
    'person': people.models.Person,
}


class LinkMixin(IFXMixin):
    model = Link
    form_class = forms.LinkForm
    template_name = 'links/link_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.entity, self.entity_model = self.get_entity_and_model()

        if self.entity_model is movies.models.Movie:
            self.parent_crumb = (_('Movies'), reverse_lazy('movies:list'))
            self.link_types_filter = {'for_movies': True}
        else:
            self.parent_crumb = (_('People'), reverse_lazy('people:list'))
            self.link_types_filter = {'for_people': True}

        self.link_types = LinkType.objects.filter(**self.link_types_filter)

        return super().dispatch(request, *args, **kwargs)

    def get_breadcrumbs(self):
        return (
            self.parent_crumb,
            (bdtitle(self.entity), self.entity.get_absolute_url()),
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['type'].queryset = self.link_types
        return form


class LinkCreateView(LinkMixin, CreateView):
    def get_entity_and_model(self):
        model = ENTITY_MODELS[self.kwargs['entity_type']]
        o = get_object_or_404(model, pk=self.kwargs['entity_pk'])
        return o, model

    def form_valid(self, form):
        with Recorder(user=self.request.user,
                      note=form.cleaned_data['editing_comment']) as r:
            form.instance.entity = self.entity
            form.save()
            r.record_addition(form.instance)
        messages.success(self.request, _("Link added successfully"))
        return redirect(self.entity)


class LinkUpdateView(LinkMixin, UpdateView):
    def get_entity_and_model(self):
        o = self.get_object().entity
        return o, o.__class__

    def form_valid(self, form):
        with Recorder(user=self.request.user,
                      note=form.cleaned_data['editing_comment']) as r:
            o = form.instance
            r.record_update_before(o.__class__.objects.get(id=o.id))
            o.entity = self.entity
            form.save()
            r.record_update_after(o)
        messages.success(self.request, _("Link updated successfully"))
        return redirect(self.entity)
