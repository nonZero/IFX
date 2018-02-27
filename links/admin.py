from django.contrib import admin

from general.templatetags.ifx import ut
from links.models import LinkType, Link


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
        'content_type',
        'entity_link',
        'value',
        'title_he',
        'title_en',
        'language',
        'limit_to_language',
        'created_at',
    )

    def entity_link(self, instance):
        return ut(instance.entity)


admin.site.register(LinkType, LinkTypeAdmin)
admin.site.register(Link, LinkAdmin)
