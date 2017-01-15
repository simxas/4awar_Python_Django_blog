from django.contrib import admin
from embed_video.admin import AdminVideoMixin

# Register your models here.
from .models import Tank

class TankModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Tank

admin.site.register(Tank, TankModelAdmin)
