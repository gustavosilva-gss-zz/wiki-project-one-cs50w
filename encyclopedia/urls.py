from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.wiki_page, name="wiki_page"),
    path("search", views.search, name="search"),
    path("new-page", views.new_page, name="new_page"),
    path("edit/<str:page>", views.edit, name="edit"),
    path("random", views.random_page, name="random")
]
