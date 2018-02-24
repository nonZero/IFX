from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView

from editing_logs.api import Recorder
from general.templatetags.ifx import bdtitle
from ifx.base_views import IFXMixin
from links import forms
from links.models import MovieLink, PersonLink, LinkType


class LinkMixin(IFXMixin):
    template_name = 'links/link_form.html'

    def get_breadcrumbs(self):
        return (
            self.parent_crumb,
            (bdtitle(self.parent), self.parent.get_absolute_url()),
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['type'].queryset = self.link_types
        return form


class LinkCreateMixin(LinkMixin):
    def dispatch(self, request, *args, **kwargs):
        self.parent = get_object_or_404(self.model.parent_model,
                                        pk=kwargs['parent_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with Recorder(user=self.request.user,
                      note=form.cleaned_data['editing_comment']) as r:
            form.instance.parent = self.parent
            form.save()
            r.record_addition(form.instance)
        messages.success(self.request, _("Link added successfully"))
        return redirect(self.parent)


class MovieLinkCreateView(LinkCreateMixin, CreateView):
    model = MovieLink
    form_class = forms.MovieLinkForm
    parent_crumb = (_('Movies'), reverse_lazy('movies:list'))
    link_types = LinkType.objects.filter(for_movies=True)


class PersonLinkCreateView(LinkCreateMixin, CreateView):
    model = PersonLink
    form_class = forms.PersonLinkForm
    parent_crumb = (_('People'), reverse_lazy('people:list'))
    link_types = LinkType.objects.filter(for_people=True)


class LinkUpdateMixin(LinkMixin):
    def dispatch(self, request, *args, **kwargs):
        self.parent = self.get_object().parent
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with Recorder(user=self.request.user,
                      note=form.cleaned_data['editing_comment']) as r:
            o = form.instance
            r.record_update_before(o.__class__.objects.get(id=o.id))
            o.parent = self.parent
            form.save()
            r.record_update_after(o)
        messages.success(self.request, _("Link updated successfully"))
        return redirect(self.parent)


class MovieLinkUpdateView(LinkUpdateMixin, UpdateView):
    model = MovieLink
    form_class = forms.MovieLinkForm
    parent_crumb = (_('Movies'), reverse_lazy('movies:list'))
    link_types = LinkType.objects.filter(for_movies=True)


class PersonLinkUpdateView(LinkUpdateMixin, UpdateView):
    model = PersonLink
    form_class = forms.PersonLinkForm
    parent_crumb = (_('People'), reverse_lazy('people:list'))
    link_types = LinkType.objects.filter(for_people=True)
