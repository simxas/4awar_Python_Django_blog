from django.contrib import admin
from embed_video.admin import AdminVideoMixin

# Register your models here.
from .models import Post, Category, CategoryToPost, Game

class CategoryToPostInline(admin.TabularInline):
    model = CategoryToPost
    extra = 1

class PostModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ["title", "timestamp", "updated"]
    list_display_links = ["timestamp", "updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]
    inlines = [CategoryToPostInline]
    class Meta:
        model = Post

class CategoryModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Category

class GameModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Game

admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Game, GameModelAdmin)
