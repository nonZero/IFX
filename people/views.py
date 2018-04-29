import django_filters
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView, FormView
from django.views.generic.detail import BaseDetailView
from django_filters.views import FilterView

from editing_logs.api import Recorder
from general.templatetags.ifx import bdtitle
from ifx.base_filters import WikidataEntityFilter
from ifx.base_views import IFXMixin, EntityEditMixin, EntityActionMixin, \
    PostToWikiDataView
from people.models import Person, Role
from wikidata_edit.upload import upload_person
from . import forms


def get_roles():
    return ((t.id, bdtitle(t)) for t in Role.objects.order_by('title_he'))


class PersonFilter(WikidataEntityFilter):
    name = django_filters.CharFilter(method='name_filter', label=_("name"))
    movies__role = django_filters.ChoiceFilter(choices=get_roles,
                                               label=_("role"))

    ordering = django_filters.OrderingFilter(
        label=_("ordering"),
        fields=(
            ('name_he', 'name_he'),
            ('name_en', 'name_en'),
        ),

        field_labels={
            'name_he': _('Hebrew Name (A -> Z)'),
            '-name_he': _('Hebrew name (Z -> A)'),
            'name_en': _('English Name (A -> Z)'),
            '-name_en': _('English name (Z -> A)'),
        }
    )

    class Meta:
        model = Person
        fields = (
            'name',
            'movies__role',
        )

    def name_filter(self, queryset, name, value):
        q = Q(name_en__icontains=value) | Q(name_he__icontains=value)
        return queryset.filter(q)


class PersonListView(IFXMixin, FilterView):
    template_name = "people/person_list.html"
    filterset_class = PersonFilter
    model = Person
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().active().filter(
            movies__isnull=False).distinct()

    def get_ordering(self):
        k = self.request.GET.get('order', None)
        if k not in PERSON_ORDER_FIELDS:
            k = "name_he"
        return k


class PersonDetailView(IFXMixin, DetailView):
    model = Person

    breadcrumbs = (
        (_("People"), reverse_lazy("people:list")),
    )

    def predispatch(self):
        if not self.get_object().active and not self.request.user.is_editor():
            raise PermissionDenied()
        super().predispatch()

    def possible_duplicates(self):
        q = Q()
        if self.object.name_he:
            q |= Q(name_he=self.object.name_he)
        if self.object.name_en:
            q |= Q(name_en=self.object.name_en)
        if not q:
            return None
        return self.model.objects.filter(q, active=True).exclude(
            id=self.object.id)


PERSON_ORDER_FIELDS = {
    'name_he',
    'name_en',
    'first_name_he',
    'first_name_en',
    'last_name_he',
    'last_name_en',
}


class PersonUpdateView(EntityEditMixin, UpdateView):
    model = Person
    breadcrumbs = PersonDetailView.breadcrumbs
    form_class = forms.PersonForm
    template_name = "generic_form.html"


class MergeIntoView(EntityActionMixin, BaseDetailView, FormView):
    model = Person
    breadcrumbs = PersonDetailView.breadcrumbs
    action_name = _("Merge into another person")
    form_class = forms.forms.Form
    template_name = "movies/movie_merge.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.other = get_object_or_404(Person, pk=self.kwargs['other'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        o = self.object  # type: Person
        if o.wikidata_id and not self.other.wikidata_id:
            form.fields['wikidata_id'] = forms.forms.BooleanField(
                required=False, initial=True,
                label=_("WikiData ID"))

        for fld in forms.MERGE_FIELDS:
            v = getattr(o, fld)
            old = getattr(self.other, fld)
            if v and v != old:
                form.fields[fld] = forms.forms.BooleanField(
                    required=False, help_text=v, initial=not old,
                    label=o._meta.get_field(fld).verbose_name)

        for r in o.movies.all():
            k = f"r_{r.id}"
            form.fields[k] = forms.forms.BooleanField(
                required=False, initial=True,
                label=f"{bdtitle(r.role)} > {bdtitle(r.movie)}")

        return form

    def form_valid(self, form):
        o = self.object  # type: Person
        d = form.cleaned_data

        with Recorder(user=self.request.user, note="merge") as r:
            r.record_update_before(o)

            if o.wikidata_id and not self.other.wikidata_id and d[
                'wikidata_id']:
                self.other.wikidata_id = o.wikidata_id
                o.wikidata_id = None
                self.other.wikidata_status = o.wikidata_status
                o.wikidata_status = o.Status.NOT_APPLICABLE

            o.active = False
            o.merged_into = self.other
            o.save()
            r.record_update_after(o)
            o.suggestions.all().delete()

            for fld in forms.MERGE_FIELDS:
                v = getattr(o, fld)
                old = getattr(self.other, fld)
                if v and v != old and d[fld]:
                    setattr(self.other, fld, v)
                    self.other.idea_modified = True

            r.record_update_before(o.__class__.objects.get(pk=self.other.pk))
            self.other.save()
            r.record_update_after(self.other)

            for ro in o.movies.all():
                k = f"r_{ro.id}"
                if d[k]:
                    mrp, created = self.other.movies.get_or_create(
                        role=ro.role, movie=ro.movie,
                        defaults={'priority': ro.priority, 'note': ro.note}
                    )
                    if created:
                        r.record_addition(mrp)
                if ro.active:
                    r.record_update_before(ro)
                    ro.active = False
                    ro.save()
                    r.record_update_after(ro)

            for l in o.links.all():
                r.record_update_before(l)
                l.entity = self.other
                l.save()
                r.record_update_after(l)

        messages.success(self.request, _("Merged."))

        return redirect(o)


class PostPersonToWikiDataView(PostToWikiDataView):
    form_class = forms.PostPersonToWikiDataForm
    model = Person
    breadcrumbs = PersonDetailView.breadcrumbs
    action_name = _("Upload to WikiData")
    fields = forms.PERSON_FIELDS
    link_type_key = 'for_people'

    # def get_initial(self):
    #     o = self.get_object()
    #     d = super().get_initial()
    #     d['desc_en'] = f"{o.year} Israeli film" if o.year else "Israeli film"
    #     d['desc_he'] = f"סרט ישראלי משנת {o.year}" if o.year else "סרט ישראלי"
    #     return d

    def upload(self, d, ids, o):
        labels = {}
        if d['name_he']:
            labels['he'] = o.name_he
        if d['name_en']:
            labels['en'] = o.name_en
        descs = {}
        if d['desc_he']:
            descs['he'] = d['desc_he']
        if d['desc_en']:
            descs['en'] = d['desc_en']
        resp = upload_person(self.request.user.get_wikidata_oauth1(),
                             labels, descs, ids, d['gender'])
        return resp
