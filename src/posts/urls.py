from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_detail,
    post_create,
)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    # url(r'^create/$', post_create),
]
