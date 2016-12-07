from django.contrib import admin
from embed_video.admin import AdminVideoMixin

# Register your models here.
from .models import Post

class PostModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ["title", "timestamp", "updated"]
    list_display_links = ["timestamp", "updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
