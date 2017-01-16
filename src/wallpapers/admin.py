from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from .models import Wallpaper, Category, CategoryToWallpaper

class CategoryToWallpaperInline(admin.TabularInline):
    model = CategoryToWallpaper
    extra = 1

class WallpaperModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Wallpaper

class CategoryModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Wallpaper

admin.site.register(Wallpaper, WallpaperModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
