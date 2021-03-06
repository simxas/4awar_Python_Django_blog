from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from .models import Tank

class TankModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Tank

admin.site.register(Tank, TankModelAdmin)
