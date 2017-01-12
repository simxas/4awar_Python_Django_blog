from django.conf.urls import url
from django.contrib import admin

from .views import (
    games,
    game_create,
    game_detail,
    game_update,
    game_delete,
)

urlpatterns = [
    url(r'^$', games, name='games'),
    url(r'^create/$', game_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', game_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', game_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', game_delete),
]
