from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.getPage, name="getPage"),
    path("search", views.search, name="search"),
    path("create", TemplateView.as_view(template_name="encyclopedia/create.html"), name="create"),
    path("addEntry", views.create, name="addEntry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("aleatorio", views.aleatorio, name="aleatorio")
]
