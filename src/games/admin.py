from django.contrib import admin
from embed_video.admin import AdminVideoMixin

# Register your models here.
from .models import Game

class GameModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Game

admin.site.register(Game, GameModelAdmin)
