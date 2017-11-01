from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create$', views.create, name="create"),
    url(r'^logging_in$', views.logging_in, name="logging_in"),
    url(r'^success$', views.success, name="success"),
    url(r'^logout$', views.logout, name="logout"),
]