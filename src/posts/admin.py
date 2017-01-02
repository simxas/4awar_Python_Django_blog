from django.contrib import admin
from embed_video.admin import AdminVideoMixin

# Register your models here.
from .models import Post, Category

class PostModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ["title", "timestamp", "updated"]
    list_display_links = ["timestamp", "updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]
    class Meta:
        model = Post

class CategoryModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Category

admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
