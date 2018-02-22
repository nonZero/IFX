from django.contrib import admin

from editing_logs.models import LogItem, LogItemRow


class LogItemRowInline(admin.StackedInline):
    model = LogItemRow
    readonly_fields = (
        'op',
        'content_type',
        'object_id',
        'entity',
        'data',
    )


class LogItemAdmin(admin.ModelAdmin):
    inlines = (
        LogItemRowInline,
    )
    readonly_fields = (
        'created_at',
        'user',
        'note',
    )


admin.site.register(LogItem, LogItemAdmin)
