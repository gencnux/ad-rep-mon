from django.contrib import admin
from .models import ReplicationLog

@admin.register(ReplicationLog)
class ReplicationLogAdmin(admin.ModelAdmin):
    list_display = ('source_server', 'target_server', 'status', 'last_checked')
    list_filter = ('status',)