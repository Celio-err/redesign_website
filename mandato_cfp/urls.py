from django.urls import path
from . import views

urlpatterns = [

    path("", views.mandato_list, name="mandato_list"),
    path("create/", views.mandato_create, name="mandato_create"),
    path("<uuid:pk>/", views.mandato_detail, name="mandato_detail"),
    path("<uuid:pk>/edit/", views.mandato_update, name="mandato_update"),
    path("<uuid:pk>/delete/", views.mandato_delete, name="mandato_delete"),

    path("tipos/", views.tipo_mandato_list, name="tipo_mandato_list"),
    path("tipos/create/", views.tipo_mandato_create, name="tipo_mandato_create"),
    path("tipos/<uuid:pk>/", views.tipo_mandato_detail, name="tipo_mandato_detail"),
    path("tipos/<uuid:pk>/edit/", views.tipo_mandato_update, name="tipo_mandato_update"),
    path("tipos/<uuid:pk>/delete/", views.tipo_mandato_delete, name="tipo_mandato_delete"),
    
    path("funcoes/", views.funcao_mandato_list, name="funcao_mandato_list"),
    path("funcoes/create/", views.funcao_mandato_create, name="funcao_mandato_create"),
    path("funcoes/<uuid:pk>/", views.funcao_mandato_detail, name="funcao_mandato_detail"),
    path("funcoes/<uuid:pk>/edit/", views.funcao_mandato_update, name="funcao_mandato_update"),
    path("funcoes/<uuid:pk>/delete/", views.funcao_mandato_delete, name="funcao_mandato_delete"),
]