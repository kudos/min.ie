from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'links.views.home', name='home'),
    url(r'(.*)', 'links.views.catchall', name='short'),
)
