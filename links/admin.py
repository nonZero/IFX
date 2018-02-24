from django.contrib import admin

from general.templatetags.ifx import ut
from links.models import LinkType, MovieLink, PersonLink


class LinkTypeAdmin(admin.ModelAdmin):
    list_display = (
        'title_he',
        'title_en',
        'slug',
        'priority',
        'title_required',
        'for_movies',
        'for_people',
        'wikidata_id',
    )


class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'parent_link',
        'value',
        'title_he',
        'title_en',
        'language',
        'limit_to_language',
        'created_at',
    )


    def parent_link(self, instance):
        return ut(instance.parent)


admin.site.register(LinkType, LinkTypeAdmin)
admin.site.register(MovieLink, LinkAdmin)
admin.site.register(PersonLink)
