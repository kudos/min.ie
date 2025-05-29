from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'(.*)', views.catchall, name='short'),
]
