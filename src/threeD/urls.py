from django.conf.urls import url
from django.contrib import admin

from .views import (
    tank_create,
    tank_360,
    tank_update,
    tank_delete
)

urlpatterns = [
    url(r'^create/$', tank_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', tank_360, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', tank_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', tank_delete),
]
