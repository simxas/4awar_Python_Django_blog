from django.contrib import admin
from embed_video.admin import AdminVideoMixin

# Register your models here.
from .models import Game, Category, CategoryToGame

class CategoryToGameInline(admin.TabularInline):
    model = CategoryToGame
    extra = 1

class GameModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Game

class CategoryModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title"]
    list_editable = ["title"]
    class Meta:
        model = Game

admin.site.register(Game, GameModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
