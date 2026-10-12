from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path("tipo/<uuid:pk>/", views.mandato_list_by_tipo, name="mandato_list_by_tipo"),
    # path("noticias/", views.noticias_publico_lista, name="noticias_publico_lista"),
    path("noticias/<uuid:pk>/", views.noticias_publico_lista, name="noticias_lis_by_tipo"),
    path("dddo/", views.dddo_publico_list, name="dddo_publico_list"),
    path("documentos-publicos/", views.documentos_publicos_publico_list, name="documentos_publicos_publico_list"),
    path("dddo/tipo/<uuid:pk>/", views.dddo_list_by_tipo, name="dddo_list_by_tipo"),
    path("detallu-noticia/<uuid:pk>/", views.noticia_detalho, name="noticia_detalho"),
    path("todas-noticias/", views.todas_noticias, name="todas_noticias"),
    path("<uuid:pk>/download/", views.documentos_publicos_review, name="documentos_publicos_review"),
    path("detallu-mandatu/<uuid:pk>/", views.detallu_mandatu, name="detail_mandatu"),
    path("contacto/", views.contacto, name="kontaktu"),
    path('i18n/', include ('django.conf.urls.i18n')),
]
