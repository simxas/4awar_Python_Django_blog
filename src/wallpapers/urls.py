from django.conf.urls import url
from django.contrib import admin

from .views import (
    wallpapers,
    wallpaper_create,
    wallpaper_detail,
    wallpaper_category,
    wallpaper_update,
    wallpaper_delete,
)

urlpatterns = [
    url(r'^$', wallpapers, name='wallpapers'),
    url(r'^create/$', wallpaper_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', wallpaper_detail, name='detail'),
    url(r'^category/(?P<slug>[\w-]+)/$', wallpaper_category, name='category'),
    url(r'^(?P<slug>[\w-]+)/edit/$', wallpaper_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', wallpaper_delete),
]
