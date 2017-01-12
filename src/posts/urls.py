from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_detail,
    post_category,
    post_create,
    post_update,
    post_delete,
    games,
    game,
    game_create,
    game_update,
    game_delete,
)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create, name='create'),
    url(r'^create_game/$', game_create, name='game_create'),
    url(r'^games/$', games, name='games'),
    url(r'^game/(?P<slug>[\w-]+)/$', game, name='game'),
    url(r'^(?P<slug>[\w-]+)/edit_game/$', game_update, name='game_update'),
    url(r'^(?P<slug>[\w-]+)/delete_game/$', game_delete),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^category/(?P<slug>[\w-]+)/$', post_category, name='category'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]
