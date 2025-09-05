from django.contrib import admin
from .models import Task, Space
from django.contrib.admin.sites import NotRegistered

class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    ordering = ('-created',)
    search_fields = ('name',)
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

class TaskAdmin(admin.ModelAdmin):
    list_display = ("short_description", "status", "workspace", "priority", "is_working")
    list_filter = ("status", "workspace", "priority", "is_working")
    search_fields = ("short_description", "description", "comments")
    readonly_fields = ()
    fieldsets = (
        (None, {
            'fields': ('short_description', 'description', 'status', 'workspace', 'priority', 'is_working', 'comments')
        }),
    )

admin.site.register(Space, SpaceAdmin)
# Unregister Task only if previously registered (safe import)
try:
    admin.site.unregister(Task)
except NotRegistered:
    pass

admin.site.register(Task, TaskAdmin)

admin.site.site_header = "Kanban Board Admin"
admin.site.index_title = "Kanban Board Administration"
admin.site.site_title = "Kanban Board Admin Portal"
