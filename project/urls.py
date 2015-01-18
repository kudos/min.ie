from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'(.*)', 'app.views.catchall', name='short'),
)
