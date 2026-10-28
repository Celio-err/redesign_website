from django.urls import path
from . import views

urlpatterns = [

    path("noticias_list", views.noticias_list, name="noticias_list"),
    path("create/", views.noticias_create, name="noticias_create"),
    path("<uuid:pk>/", views.noticias_detail, name="noticia_detail"),
    path("<uuid:pk>/edit/", views.noticias_create, name="noticias_update"),
    path("<uuid:pk>/delete/", views.noticias_delete, name="noticias_delete"),
    path("tipos/", views.tipo_noticias_list, name="tipo_noticias_list"),
    path("tipos/create/", views.tipo_noticias_create, name="tipo_noticias_create"),
    path("tipos/<uuid:pk>/", views.tipo_noticias_detail, name="tipo_noticias_detail"),
    path("tipos/<uuid:pk>/edit/", views.tipo_noticias_update, name="tipo_noticias_update"),
    path("tipos/<uuid:pk>/delete/", views.tipo_noticias_delete, name="tipo_noticias_delete"),
]