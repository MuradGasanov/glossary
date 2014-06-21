__author__ = 'murad'

from django.conf.urls import patterns, include, url
from main_app.views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^get_titles/$', get_titles),
    url(r'^login/$', log_in),
    url(r'^logout/$', log_out),
    url(r'^term/read/$', get_terms),
    url(r'^term/create/$', create_term),
    url(r'^term/update/$', update_term),
    url(r'^term/remove/$', remove_term),
    url(r'^term/get_projects/$', get_projects),
    url(r'^search_suggestions/$', search_suggestions),
)