from django.contrib import admin

from links.models import LinkType, MovieLink, PersonLink

admin.site.register(LinkType)
admin.site.register(MovieLink)
admin.site.register(PersonLink)
