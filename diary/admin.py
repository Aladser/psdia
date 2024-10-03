from django.contrib import admin
from diary.models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'content', 'created_at', 'updated_at')
    search_fields = ('owner', 'content')
