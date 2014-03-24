__author__ = 'murad'

from django.conf.urls import patterns, include, url
from main_app.views import *

urlpatterns = patterns('',
    url(r'^$', index),
)