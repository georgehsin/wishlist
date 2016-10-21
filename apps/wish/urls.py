from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^home$', views.home),
    url(r'^wish_items/create$', views.create),
    url(r'^wish_items/(?P<id>[0-9]+)$', views.product),
    url(r'^adding$', views.adding),
    url(r'^add/(?P<id>[0-9]+)$', views.selfadd),
    url(r'^delete/(?P<id>[0-9]+)$', views.delete),
    url(r'^logout$', views.logout),
]