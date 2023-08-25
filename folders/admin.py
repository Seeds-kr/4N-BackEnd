from django.contrib import admin
from .models import Folder


class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_locations', 'created', 'updated')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('locations')

    def display_locations(self, obj):
        return ", ".join([location.name for location in obj.locations.all()])

    display_locations.short_description = "저장된 장소"


admin.site.register(Folder, FolderAdmin)
