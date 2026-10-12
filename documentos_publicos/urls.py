from django.urls import path
from . import views

urlpatterns = [

    path("", views.documentos_publicos_list, name="documentos_publicos_list"),
    path("create/", views.documentos_publicos_create, name="documentos_publicos_create"),
    path("<uuid:pk>/", views.documentos_publicos_detail, name="documentos_publicos_detail"),
    path("<uuid:pk>/edit/", views.documentos_publicos_update, name="documentos_publicos_update"),
    path("<uuid:pk>/delete/", views.documentos_publicos_delete, name="documentos_publicos_delete"),

    path("tipos/", views.tipo_documentos_publicos_list, name="tipo_documentos_publicos_list"),
    path("tipos/create/", views.tipo_documentos_publicos_create, name="tipo_documentos_publicos_create"),
    path("tipos/<uuid:pk>/", views.tipo_documentos_publicos_detail, name="tipo_documentos_publicos_detail"),
    path("tipos/<uuid:pk>/edit/", views.tipo_documentos_publicos_update, name="tipo_documentos_publicos_update"),
    path("tipos/<uuid:pk>/delete/", views.tipo_documentos_publicos_delete, name="tipo_documentos_publicos_delete"),
    path("<uuid:pk>/download/", views.documentos_publicos_review, name="documentos_publicos_review"),
]