from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add$', views.add, name="add"),
    url(r'^(?P<item_id>\d+)$', views.show, name="show"),
    url(r'^itemcreate$', views.itemcreate, name="itemcreate"),
    url(r'^new$', views.new, name="new"),
    url(r'^remove$', views.remove, name="remove"),
    url(r'^delete$', views.delete, name="delete"),
]


#for show and remove, I need to display the item id. I'll also have to go back and fix this in html and views files
#Dont forget to add messages on all HTML pages