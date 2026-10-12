from django.urls import path
from . import views

urlpatterns = [

    path("dddo/", views.documentos_dddo_list, name="documentos_dddo_list"),
    path("create/", views.documentos_dddo_create, name="documentos_dddo_create"),
    path("<uuid:pk>/", views.documentos_dddo_detail, name="documentos_dddo_detail"),
    path("<uuid:pk>/edit/", views.documentos_dddo_update, name="documentos_dddo_update"),
    path("<uuid:pk>/delete/", views.documentos_dddo_delete, name="documentos_dddo_delete"),
    path("<uuid:pk>/download/", views.documentos_dddo_download, name="documentos_dddo_download"),

    path("tipos/", views.tipo_dddo_list, name="tipo_dddo_list"),
    path("tipos/create/", views.tipo_dddo_create, name="tipo_dddo_create"),
    path("tipos/<uuid:pk>/", views.tipo_dddo_detail, name="tipo_dddo_detail"),
    path("tipos/<uuid:pk>/edit/", views.tipo_dddo_update, name="tipo_dddo_update"),
    path("tipos/<uuid:pk>/delete/", views.tipo_dddo_delete, name="tipo_dddo_delete"),
]